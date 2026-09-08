#!/usr/bin/env python3
"""Diagnostics behind docs/arc-validation-remedies.html.

Extends scripts/arc_error_map.py in four ways, all on the same "horizontal" runs
(arc laid flat, prop axis vertical, so every mic should read the same):

1. Tones vs broadband. The blade-passage frequency (BPF) and its harmonics are
   located in each capture, the tone levels and the tone-free (notched) band
   levels are fitted separately with the same run + position + mic model. A
   reflection bends everything at that frequency; a distorted rotor inflow
   bends only the tones.
2. The tone as a swept probe. Five PWM steps x six harmonics give ~30 probe
   frequencies per position between ~150 Hz and ~1.5 kHz. The position error
   versus frequency is fitted per position with a single-echo comb,
   20 log10 |1 + a exp(-j 2 pi f D / c)| + c0, which yields the extra path D of
   the reflection seen at that position.
3. Standard errors of the position and mic terms from the least-squares
   covariance, so the maps carry error bars.
4. A cepstrum of the tone-notched broadband ripple per mic (the earlier
   cepstrum of the raw spectrum was dominated by the harmonic comb itself:
   4.2 ms = 1/BPF, 8.4 ms = the shaft period).

    scripts/arc_validation_diagnostics.py --data ../SoundVisualizer-data/data \
        --glob '2004__6in__unset__dp1-baseline-horizontal-prop*' \
        --exclude dp1-baseline-horizontal-prop{1,2,3,4,5,6} \
        --rotated dp1-baseline-horizontal-prop1{1,2,3,4} --out docs/analysis
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys

import numpy as np
from scipy.io import wavfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from server.core import calibration as C
from server.core.fft import compute_fft

C_SOUND = 343.0
THIRD_OCT = [125 * 2 ** (i / 3) for i in range(0, 19)]  # 125 Hz .. 8 kHz
NH = 6  # harmonics of BPF used as probes
FFT = 4096
FFT_FINE = 16384  # 2.9 Hz bins for the broadband estimate between the tones


def read_wav(path):
    fs, x = wavfile.read(path)
    if x.ndim > 1:
        x = x[:, 0]
    if np.issubdtype(x.dtype, np.integer):
        x = x.astype(float) / np.iinfo(x.dtype).max
    else:
        x = x.astype(float)
    return fs, x


def spectrum(x, fs, cal):
    f, mag = compute_fft(x, fs, size=FFT)
    if cal is not None:
        mag = C.apply_calibration_to_spectrum(f, mag, cal)
    return f, mag


def find_bpf(f, mags, lo=100.0, hi=320.0):
    """Blade-passage frequency from the arc-mean spectrum: the most prominent peak in
    lo..hi whose second and third harmonics are also present. Returns (f0, ok)."""
    from scipy.signal import find_peaks

    m = np.mean(mags, axis=0)
    df = f[1] - f[0]
    sel = (f > lo) & (f < hi)
    idx = np.where(sel)[0]
    pk, pr = find_peaks(m[sel], prominence=8)
    if len(pk) == 0:
        return None, False
    order = np.argsort(pr["prominences"])[::-1]
    for o in order:
        k = idx[pk[o]]
        f0 = f[k]
        # refine with a parabola
        y0, y1, y2 = m[k - 1], m[k], m[k + 1]
        denom = y0 - 2 * y1 + y2
        if abs(denom) > 1e-9:
            f0 = f[k] + 0.5 * (y0 - y2) / denom * df
        good = 0
        for h in (2, 3):
            win = np.abs(f - h * f0) <= 2 * df
            near = (np.abs(f - h * f0) > 4 * df) & (np.abs(f - h * f0) <= 12 * df)
            if m[win].max() - np.median(m[near]) > 8:
                good += 1
        if good == 2:
            # refine f0 from harmonics 1..4 (weighted mean of peak positions / h)
            ests, ws = [], []
            for h in range(1, 5):
                win = np.abs(f - h * f0) <= 2 * df
                kk = np.where(win)[0][np.argmax(m[win])]
                if 1 <= kk < len(m) - 1:
                    y0, y1, y2 = m[kk - 1], m[kk], m[kk + 1]
                    denom = y0 - 2 * y1 + y2
                    fp = f[kk] + (0.5 * (y0 - y2) / denom * df if abs(denom) > 1e-9 else 0.0)
                    ests.append(fp / h)
                    ws.append(h)
            return float(np.average(ests, weights=ws)), True
    return None, False


def tone_and_broadband(f, mag, f0):
    """Per-harmonic tone levels (dB), third-octave broadband levels with all shaft
    harmonics notched (dB), and the ripple spectrum for the cepstrum."""
    df = f[1] - f[0]
    lin = 10 ** (mag / 10)
    tones = []
    for h in range(1, NH + 1):
        sel = np.abs(f - h * f0) <= 3 * df
        tones.append(10 * np.log10(lin[sel].sum() * df + 1e-30))
    # notch every multiple of the shaft frequency (f0/2), +-4 bins, up to 8 kHz
    mask = np.ones_like(f, dtype=bool)
    k = 1
    while k * f0 / 2 < 8500:
        w = 3 if k % 2 == 0 else 2  # BPF harmonics vs shaft harmonics
        mask &= np.abs(f - k * f0 / 2) > w * df
        k += 1
    bb = []
    for fc in THIRD_OCT:
        band = (f >= fc / 2 ** (1 / 6)) & (f < fc * 2 ** (1 / 6))
        kept = band & mask
        if kept.sum() == 0:
            bb.append(np.nan)
            continue
        bb.append(10 * np.log10(lin[kept].sum() * df * band.sum() / kept.sum() + 1e-30))
    return np.array(tones), np.array(bb), mask


def local_broadband(ff, magf, f0, h, inner=7.0, outer=15.0):
    """Mean PSD (dB) in the two side windows inner..outer Hz away from harmonic h of f0,
    i.e. the broadband floor at the tone's own frequency, tone excluded."""
    d = np.abs(ff - h * f0)
    sel = (d >= inner) & (d <= outer)
    lin = 10 ** (magf[sel] / 10)
    return 10 * np.log10(lin.mean() + 1e-30)


def fine_broadband_bands(ff, magf, f0, fmax=1100.0):
    """Third-octave broadband levels below fmax from the fine spectrum, every shaft
    harmonic notched by +-3 fine bins (+-8.8 Hz)."""
    df = ff[1] - ff[0]
    lin = 10 ** (magf / 10)
    mask = np.ones_like(ff, dtype=bool)
    k = 1
    while k * f0 / 2 < fmax * 1.2:
        mask &= np.abs(ff - k * f0 / 2) > 3 * df
        k += 1
    out = []
    for fc in THIRD_OCT:
        if fc > fmax:
            out.append(np.nan)
            continue
        band = (ff >= fc / 2 ** (1 / 6)) & (ff < fc * 2 ** (1 / 6))
        kept = band & mask
        out.append(10 * np.log10(lin[kept].sum() * df * band.sum() / kept.sum() + 1e-30) if kept.sum() else np.nan)
    return np.array(out)


def load(data, pattern, exclude):
    cals = {}
    for t in glob.glob(os.path.join(data, "calibrations", "*.txt")):
        with open(t) as fh:
            cals[os.path.basename(t)[:-4]] = C.parse_umik_calibration(fh.read())
    caps = []  # one entry per (run, pwm): dict with per-mic arrays
    for key in sorted(glob.glob(os.path.join(data, pattern)), key=os.path.getmtime):
        name = os.path.basename(key).split("__")[-1]
        if name in exclude:
            continue
        metas = []
        for m in glob.glob(os.path.join(key, "measurements", "*acoustic*", "meta.json")):
            with open(m) as fh:
                metas.append((json.load(fh), os.path.dirname(m)))
        by_cap = {}
        for m, d in metas:
            cid = os.path.basename(d).split("__")[0]
            by_cap.setdefault((m["pwm_setpoint"], cid), []).append((m, d))
        # last usable capture per pwm (aborted captures leave WAVs of 0.01-0.4 s; 0.5 s still gives 12 Welch segments)
        last = {}
        for (pwm, cid), lst in by_cap.items():
            ok = all(len(read_wav(os.path.join(d, "audio.wav"))[1]) >= 0.5 * 48000 for _, d in lst)
            if ok and (pwm not in last or cid > last[pwm][0]):
                last[pwm] = (cid, lst)
        starts = sorted(cid for cid, _ in last.values())
        for pwm, (cid, lst) in last.items():
            mics = []
            for m, d in lst:
                fs, x = read_wav(os.path.join(d, "audio.wav"))
                cal = cals.get(m["calibration_file_id"])
                f, mag = spectrum(x, fs, cal)
                ff, magf = compute_fft(x, fs, size=FFT_FINE)
                if cal is not None:
                    magf = C.apply_calibration_to_spectrum(ff, magf, cal)
                # first and second half of the capture, for the time trend
                n = len(x) // 2
                _, mag_a = spectrum(x[:n], fs, cal)
                _, mag_b = spectrum(x[n:], fs, cal)
                mics.append(dict(serial=m["calibration_file_id"], elev=float(m["elevation_deg"]), f=f, mag=mag, ff=ff, magf=magf, mag_a=mag_a, mag_b=mag_b))
            caps.append(dict(run=name, pwm=pwm, cid=cid, seq=starts.index(cid), mics=mics))
    return caps


def fit(obs, rotated):
    """obs: list of (run, elev, serial, vector). Returns runs, poss, sers, P, M, R, SE_P, SE_M."""
    runs = sorted({o[0] for o in obs})
    poss = sorted({o[1] for o in obs})
    sers = sorted({o[2] for o in obs})
    n = len(runs) + len(poss) + len(sers)
    A = np.zeros((len(obs), n))
    Y = np.array([o[3] for o in obs])
    for i, (r, e, s, _) in enumerate(obs):
        p = -e if r in rotated else e
        A[i, runs.index(r)] = 1
        A[i, len(runs) + poss.index(p)] = 1
        A[i, len(runs) + len(poss) + sers.index(s)] = 1
    c1 = np.zeros(n)
    c1[len(runs) : len(runs) + len(poss)] = 10
    c2 = np.zeros(n)
    c2[len(runs) + len(poss) :] = 10
    Aa = np.vstack([A, c1, c2])
    Ya = np.vstack([Y, np.zeros((2, Y.shape[1]))])
    X = np.linalg.lstsq(Aa, Ya, rcond=None)[0]
    R = Y - A @ X
    dof = max(len(obs) - (n - 2), 1)
    s2 = (R**2).sum(axis=0) / dof  # per column (band / frequency)
    cov_unit = np.linalg.pinv(Aa.T @ Aa)
    se = np.sqrt(np.outer(np.diag(cov_unit), s2))
    P = X[len(runs) : len(runs) + len(poss)]
    M = X[len(runs) + len(poss) :]
    return runs, poss, sers, P, M, R, se[len(runs) : len(runs) + len(poss)], se[len(runs) + len(poss) :]


def comb_fit(fr, dev, w=None):
    """Fit dev(f) = 20 log10 |1 + a exp(-j k D)| + c0 (weighted). Grid over D and a, c0 closed form."""
    fr = np.asarray(fr)
    dev = np.asarray(dev)
    w = np.ones_like(dev) if w is None else np.asarray(w)
    best = None
    for D in np.arange(0.05, 4.0, 0.01):
        ph = np.exp(-2j * np.pi * fr * D / C_SOUND)
        for a in np.arange(0.05, 0.95, 0.025):
            model = 20 * np.log10(np.abs(1 + a * ph))
            c0 = np.sum(w * (dev - model)) / np.sum(w)
            rss = np.sum(w * (dev - model - c0) ** 2)
            if best is None or rss < best[0]:
                best = (rss, D, a, c0)
    rss, D, a, c0 = best
    rms0 = np.sqrt(np.sum(w * (dev - np.sum(w * dev) / np.sum(w)) ** 2) / np.sum(w))
    return dict(D=D, a=a, c0=c0, rms=np.sqrt(rss / np.sum(w)), rms0=rms0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--glob", required=True)
    ap.add_argument("--rotated", nargs="*", default=[])
    ap.add_argument("--exclude", nargs="*", default=[])
    ap.add_argument("--out", default="docs/analysis")
    a = ap.parse_args()
    rot = set(a.rotated)
    caps = load(a.data, a.glob, set(a.exclude))
    if not caps:
        sys.exit("no captures")
    os.makedirs(a.out, exist_ok=True)
    report = {}

    # ---- BPF per capture, tone + broadband levels per mic
    for cp in caps:
        f = cp["mics"][0]["f"]
        cp["bpf"], cp["tone_ok"] = find_bpf(f, [m["mag"] for m in cp["mics"]])
        for m in cp["mics"]:
            df = f[1] - f[0]
            lin = 10 ** (m["mag"] / 10)
            m["tob"] = np.array([10 * np.log10(lin[(f >= fc / 2 ** (1 / 6)) & (f < fc * 2 ** (1 / 6))].sum() * df) for fc in THIRD_OCT])
            if cp["tone_ok"]:
                m["tones"], m["bb"], m["mask"] = tone_and_broadband(f, m["mag"], cp["bpf"])
                m["tones_a"], _, _ = tone_and_broadband(f, m["mag_a"], cp["bpf"])
                m["tones_b"], _, _ = tone_and_broadband(f, m["mag_b"], cp["bpf"])
                m["lbb"] = np.array([local_broadband(m["ff"], m["magf"], cp["bpf"], h) for h in range(1, NH + 1)])
                m["bbf"] = fine_broadband_bands(m["ff"], m["magf"], cp["bpf"])
            else:
                m["tones"] = np.full(NH, np.nan)
                m["bb"] = m["tob"].copy()
                m["mask"] = np.ones_like(f, dtype=bool)
    pwms = sorted({cp["pwm"] for cp in caps})
    runs_all = sorted({cp["run"] for cp in caps}, key=lambda r: int(r.replace("dp1-baseline-horizontal-prop", "")))
    print("BPF per run and PWM step (Hz; '-' = no tone found, 'x' = capture missing/aborted):")
    print(f"{'run':>8} " + " ".join(f"{p:>6}" for p in pwms))
    bpf_table = {}
    for r in runs_all:
        row = []
        for p in pwms:
            c = [cp for cp in caps if cp["run"] == r and cp["pwm"] == p]
            row.append("x" if not c else (f"{c[0]['bpf']:.0f}" if c[0]["tone_ok"] else "-"))
        bpf_table[r] = row
        print(f"{r[-6:]:>8} " + " ".join(f"{v:>6}" for v in row))
    report["bpf_table"] = dict(pwms=pwms, rows=bpf_table)
    tone_pwms = [p for p in pwms if sum(cp["tone_ok"] for cp in caps if cp["pwm"] == p) >= 5]
    report["tone_pwms"] = tone_pwms
    bpf_by_pwm = {p: [cp["bpf"] for cp in caps if cp["pwm"] == p and cp["tone_ok"]] for p in tone_pwms}
    report["bpf_by_pwm"] = {str(p): dict(mean=float(np.mean(v)), min=float(np.min(v)), max=float(np.max(v)), n=len(v)) for p, v in bpf_by_pwm.items()}
    print("\nTone PWM steps:", {p: f"BPF {np.mean(v):.0f} Hz ({np.min(v):.0f}-{np.max(v):.0f}), n={len(v)}" for p, v in bpf_by_pwm.items()})

    # ---- (1) tones vs broadband, per PWM step: joint fits
    probe = {}  # (pwm, h) -> dict(f, P, SE, ...)
    bbfit = {}
    tobfit = {}
    for p in pwms:
        sub = [cp for cp in caps if cp["pwm"] == p]
        obs_b = [(cp["run"], m["elev"], m["serial"], m["bb"]) for cp in sub for m in cp["mics"]]
        obs_o = [(cp["run"], m["elev"], m["serial"], m["tob"]) for cp in sub for m in cp["mics"]]
        runs, poss, sers, Pb, Mb, Rb, sePb, seMb = fit(obs_b, rot)
        bbfit[p] = dict(P=Pb, se=sePb, M=Mb, res=np.sqrt(np.mean(Rb**2, axis=0)), n=len(sub))
        runs, poss, sers, Po, Mo, Ro, sePo, seMo = fit(obs_o, rot)
        tobfit[p] = dict(P=Po, se=sePo, M=Mo, res=np.sqrt(np.mean(Ro**2, axis=0)), n=len(sub))
        if p in tone_pwms:
            subt = [cp for cp in sub if cp["tone_ok"]]
            fmed = np.median([cp["bpf"] for cp in subt])
            dropped = [cp["run"] for cp in subt if abs(cp["bpf"] / fmed - 1) > 0.03]
            subt = [cp for cp in subt if abs(cp["bpf"] / fmed - 1) <= 0.03]
            if dropped:
                print(f"  PWM {p}: dropped from the tone fit (BPF more than 3% off the median {fmed:.0f} Hz): {dropped}")
            obs_t = [(cp["run"], m["elev"], m["serial"], m["tones"]) for cp in subt for m in cp["mics"]]
            runs, poss, sers, P, M, R, seP, seM = fit(obs_t, rot)
            obs_l = [(cp["run"], m["elev"], m["serial"], m["lbb"]) for cp in subt for m in cp["mics"]]
            _, _, _, Pl, Ml, Rl, sePl, seMl = fit(obs_l, rot)
            obs_f = [(cp["run"], m["elev"], m["serial"], m["bbf"]) for cp in subt for m in cp["mics"]]
            _, _, _, Pf, Mf, Rf, sePf, seMf = fit(obs_f, rot)
            bbfit[p]["Pfine"] = Pf
            bbfit[p]["sefine"] = sePf
            fmean = np.mean([cp["bpf"] for cp in subt])
            fsd = np.std([cp["bpf"] for cp in subt])
            for h in range(NH):
                probe[(p, h + 1)] = dict(f=fmean * (h + 1), fsd=fsd * (h + 1), P=P[:, h], se=seP[:, h], M=M[:, h], seM=seM[:, h], res=float(np.sqrt(np.mean(R[:, h] ** 2))), n=len(subt), Pl=Pl[:, h], sel=sePl[:, h], resl=float(np.sqrt(np.mean(Rl[:, h] ** 2))))
    poss = sorted({-m["elev"] if cp["run"] in rot else m["elev"] for cp in caps for m in cp["mics"]})
    sers = sorted({m["serial"] for cp in caps for m in cp["mics"]})

    # all-PWM broadband fit (the reflection should not depend on RPM); below 1.1 kHz the
    # fine-resolution notched bands are used, above it the 4096-point ones
    for cp in caps:
        for m in cp["mics"]:
            if cp["tone_ok"]:
                m["bbm"] = np.where(np.array(THIRD_OCT) <= 1100, m["bbf"], m["bb"])
            else:
                m["bbm"] = m["bb"]
    obs_b_all = [(f"{cp['run']}@{cp['pwm']}", m["elev"], m["serial"], m["bbm"]) for cp in caps for m in cp["mics"]]
    rot_all = {f"{r}@{p}" for r in rot for p in pwms}
    _, _, _, Pb_all, Mb_all, Rb_all, sePb_all, seMb_all = fit(obs_b_all, rot_all)
    obs_o_all = [(f"{cp['run']}@{cp['pwm']}", m["elev"], m["serial"], m["tob"]) for cp in caps for m in cp["mics"]]
    _, _, _, Po_all, Mo_all, Ro_all, sePo_all, seMo_all = fit(obs_o_all, rot_all)

    head = "," + ",".join(f"{fc:.0f}Hz" for fc in THIRD_OCT)
    np.savetxt(os.path.join(a.out, "remedies-broadband-position-map-allpwm.csv"), np.column_stack([poss, Pb_all]), delimiter=",", header="position_deg" + head, comments="", fmt="%.2f")
    np.savetxt(os.path.join(a.out, "remedies-broadband-position-se-allpwm.csv"), np.column_stack([poss, sePb_all]), delimiter=",", header="position_deg" + head, comments="", fmt="%.2f")
    np.savetxt(os.path.join(a.out, "remedies-thirdoct-position-map-allpwm.csv"), np.column_stack([poss, Po_all]), delimiter=",", header="position_deg" + head, comments="", fmt="%.2f")
    np.savetxt(os.path.join(a.out, "remedies-thirdoct-position-se-pwm1900.csv"), np.column_stack([poss, tobfit[1900]["se"]]), delimiter=",", header="position_deg" + head, comments="", fmt="%.2f")
    np.savetxt(os.path.join(a.out, "remedies-mic-offsets-pwm1900.csv"), np.column_stack([[int(x) for x in sers], tobfit[1900]["M"]]), delimiter=",", header="serial" + head, comments="", fmt="%.2f")
    np.savetxt(os.path.join(a.out, "remedies-mic-offsets-se-pwm1900.csv"), np.column_stack([[int(x) for x in sers], tobfit[1900]["se"] if False else seMo_all]), delimiter=",", header="serial" + head, comments="", fmt="%.2f")
    print("\nStandard errors (dB) of the position term at PWM 1900, third-octave: median %.2f, max %.2f" % (np.median(tobfit[1900]["se"]), tobfit[1900]["se"].max()))
    print("Standard errors (dB) of the mic term, all 60 captures: median %.2f, max %.2f" % (np.median(seMo_all), seMo_all.max()))
    report["se_position_pwm1900_thirdoct"] = dict(median=float(np.median(tobfit[1900]["se"])), max=float(tobfit[1900]["se"].max()))
    report["se_mic_allpwm_thirdoct"] = dict(median=float(np.median(seMo_all)), max=float(seMo_all.max()))

    # probe table (position x frequency) sorted by frequency
    keys = sorted(probe, key=lambda k: probe[k]["f"])
    Fp = np.array([probe[k]["f"] for k in keys])
    Pp = np.column_stack([probe[k]["P"] for k in keys])
    SEp = np.column_stack([probe[k]["se"] for k in keys])
    with open(os.path.join(a.out, "remedies-tone-probe-map.csv"), "w") as fh:
        fh.write("position_deg," + ",".join(f"{probe[k]['f']:.0f}Hz(pwm{k[0]}h{k[1]})" for k in keys) + "\n")
        for i, p in enumerate(poss):
            fh.write(f"{p:.0f}," + ",".join(f"{v:.2f}" for v in Pp[i]) + "\n")
        fh.write("se_mean," + ",".join(f"{v:.2f}" for v in SEp.mean(axis=0)) + "\n")
        fh.write("residual_rms," + ",".join(f"{probe[k]['res']:.2f}" for k in keys) + "\n")
    print("\nTone probe map (room term per position at each BPF harmonic), dB from a circle:")
    print(f"{'pos':>5} " + " ".join(f"{probe[k]['f']:6.0f}" for k in keys))
    for i, p in enumerate(poss):
        print(f"{p:>+5.0f} " + " ".join(f"{v:+6.1f}" for v in Pp[i]))
    print(f"{'se':>5} " + " ".join(f"{v:6.1f}" for v in SEp.mean(axis=0)))
    print(f"{'rms':>5} " + " ".join(f"{np.sqrt(np.mean(Pp[:, j] ** 2)):6.1f}" for j in range(len(keys))) + "   (spread of the room term across positions)")

    # frequency correlation of the position pattern: how fast does the room pattern change with frequency?
    corr = []
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            if Fp[j] / Fp[i] < 2.0:
                r = np.corrcoef(Pp[:, i], Pp[:, j])[0, 1]
                corr.append((float(Fp[i]), float(Fp[j]), float(r)))
    report["pattern_correlation_vs_frequency"] = corr
    print("\nCorrelation of the position pattern between nearby probe frequencies (f1, f2, r):")
    for f1, f2, r in sorted(corr, key=lambda t: t[1] / t[0])[:14]:
        print(f"  {f1:6.0f} {f2:6.0f}  ratio {f2 / f1:.3f}  r={r:+.2f}")

    # ---- (2) comb fit per position on the probes (130 Hz .. 1.6 kHz), weighted 1/SE^2
    combs = {}
    for i, p in enumerate(poss):
        sel = (Fp >= 130) & (Fp <= 1600) & (SEp[i] < 2.0)
        combs[p] = comb_fit(Fp[sel], Pp[i, sel], 1.0 / np.maximum(SEp[i, sel], 0.3) ** 2)
    report["comb_fits"] = {str(p): {k: float(v) for k, v in c.items()} for p, c in combs.items()}
    print("\nSingle-echo comb fit per position (probe tones 130-1600 Hz, weighted):")
    print(f"{'pos':>5} {'D m':>6} {'a':>5} {'rms0':>5} {'rms':>5}")
    for p in poss:
        c = combs[p]
        print(f"{p:>+5.0f} {c['D']:6.2f} {c['a']:5.2f} {c['rms0']:5.2f} {c['rms']:5.2f}")

    # ---- (3) tone vs broadband discriminant in the BPF band and its 2nd harmonic at each tone PWM
    print("\nPosition error at the tone frequency: BPF-harmonic tone vs the broadband floor 7-15 Hz beside it (dB from a circle):")
    disc = []
    for p in tone_pwms:
        for h in (1, 2, 3):
            fb = probe[(p, h)]["f"]
            bi = int(np.argmin([abs(np.log(fb / fc)) for fc in THIRD_OCT]))
            row = dict(pwm=p, h=h, f=fb, band=THIRD_OCT[bi], tone=probe[(p, h)]["P"].tolist(), tone_se=probe[(p, h)]["se"].tolist(), bb=probe[(p, h)]["Pl"].tolist(), bb_se=probe[(p, h)]["sel"].tolist(), band_bb=bbfit[p]["Pfine"][:, bi].tolist(), band_bb_se=bbfit[p]["sefine"][:, bi].tolist(), tob=tobfit[p]["P"][:, bi].tolist())
            disc.append(row)
            r = np.corrcoef(row["tone"], row["bb"])[0, 1]
            print(f"pwm {p} h{h} {fb:.0f} Hz: tone rms {np.sqrt(np.mean(np.square(row['tone']))):.1f} / local-bb rms {np.sqrt(np.mean(np.square(row['bb']))):.1f} / band-bb rms {np.sqrt(np.nanmean(np.square(row['band_bb']))):.1f}, corr(tone, local bb) {r:+.2f} | " + " ".join(f"{q:+.0f}:{t:+.1f}/{b:+.1f}" for q, t, b in zip(poss, row["tone"], row["bb"])))
    report["bpf_band_tone_vs_broadband"] = disc

    # ---- (4) time trend within captures and sequence position (tone captures only, relative to same-PWM mean)
    dif = []
    for cp in caps:
        if not cp["tone_ok"]:
            continue
        for m in cp["mics"]:
            dif.append(m["tones_b"][:4] - m["tones_a"][:4])
    dif = np.array(dif)
    report["tone_second_half_minus_first_half_dB"] = dict(mean=dif.mean(axis=0).tolist(), sd=dif.std(axis=0).tolist(), n=int(len(dif)))
    print("\nTone level, second half of capture minus first half (tone captures, all mics), h1..h4: mean", np.round(dif.mean(axis=0), 2), "sd", np.round(dif.std(axis=0), 2), "n", len(dif))
    seqs = {}
    for p in tone_pwms:
        subt = [cp for cp in caps if cp["pwm"] == p and cp["tone_ok"]]
        # per-position mean over runs (rotation-aware) of each harmonic level
        ref = {}
        for cp in subt:
            for m in cp["mics"]:
                q = -m["elev"] if cp["run"] in rot else m["elev"]
                ref.setdefault(q, []).append(m["tones"][:4])
        ref = {q: np.mean(v, axis=0) for q, v in ref.items()}
        for cp in subt:
            for m in cp["mics"]:
                q = -m["elev"] if cp["run"] in rot else m["elev"]
                seqs.setdefault(cp["seq"], []).append(m["tones"][:4] - ref[q])
    report["tone_minus_position_mean_by_sequence_index"] = {str(k): dict(mean=np.mean(v, axis=0).tolist(), n=len(v)) for k, v in sorted(seqs.items())}
    print("Tone level minus its position mean, by the step's index in the run sequence (h1..h4):", {k: (np.round(np.mean(v, axis=0), 1).tolist(), len(v)) for k, v in sorted(seqs.items())})

    # ---- (5) cepstrum of the tone-notched ripple per mic (tone captures)
    cep = {}
    q = None
    for cp in caps:
        if not cp["tone_ok"]:
            continue
        f = cp["mics"][0]["f"]
        for m in cp["mics"]:
            sel = (f >= 300) & (f <= 6000)
            mask = m["mask"]
            mag_i = np.interp(f, f[mask], m["mag"][mask])
            x = mag_i[sel]
            fl = np.log(f[sel])
            trend = np.array([x[(fl >= v - 0.115) & (fl <= v + 0.115)].mean() for v in fl])
            rip = (x - trend) * np.hanning(len(x))
            c = np.abs(np.fft.irfft(rip, n=4 * len(rip)))
            q = np.arange(len(c)) / (4 * len(rip) * (f[1] - f[0]))
            cep.setdefault(m["serial"], []).append(c)
    fig_cep = {s: np.mean(lst, axis=0) for s, lst in cep.items()}
    cep_pwm = {}
    for cp in caps:
        if not cp["tone_ok"]:
            continue
        f = cp["mics"][0]["f"]
        for m in cp["mics"]:
            sel = (f >= 300) & (f <= 6000)
            mag_i = np.interp(f, f[m["mask"]], m["mag"][m["mask"]])
            x = mag_i[sel]
            fl = np.log(f[sel])
            trend = np.array([x[(fl >= v - 0.115) & (fl <= v + 0.115)].mean() for v in fl])
            rip = (x - trend) * np.hanning(len(x))
            cep_pwm.setdefault(cp["pwm"], []).append(np.abs(np.fft.irfft(rip, n=4 * len(rip))))
    from scipy.signal import find_peaks as _fp

    cep_pwm_peaks = {}
    for p, lst in cep_pwm.items():
        arr = np.mean(lst, axis=0)
        sel = (q > 0.5e-3) & (q < 10e-3)
        pk, pr = _fp(arr[sel], prominence=np.max(arr[sel]) * 0.25)
        cep_pwm_peaks[str(p)] = [(float(q[sel][k] * 1e3), float(arr[sel][k])) for k in pk[np.argsort(pr["prominences"])[::-1][:3]]]
    report["cepstrum_peaks_by_pwm_ms"] = cep_pwm_peaks
    print("\nCepstral peaks by PWM step (a harmonic artefact scales with 1/BPF, a reflection does not):", {p: [(round(t, 2), round(v, 3)) for t, v in v_] for p, v_ in cep_pwm_peaks.items()})
    # peaks per mic between 0.5 and 10 ms
    from scipy.signal import find_peaks

    cpeaks = {}
    for s, arr in fig_cep.items():
        sel = (q > 0.5e-3) & (q < 10e-3)
        pk, pr = find_peaks(arr[sel], prominence=np.max(arr[sel]) * 0.25)
        cpeaks[s] = [(float(q[sel][k] * 1e3), float(arr[sel][k])) for k in pk[np.argsort(pr["prominences"])[::-1][:3]]]
    report["cepstrum_peaks_ms"] = cpeaks
    print("\nCepstral peaks of the tone-notched broadband ripple per mic (ms, amplitude):", {s: [(round(t, 2), round(v, 3)) for t, v in pks] for s, pks in cpeaks.items()})

    # ---- (6) image-source plane fit on the comb D per position
    def plane_D(r, d, phi, th):
        thr = np.radians(th)
        img = 2 * d * np.array([np.cos(np.radians(phi)), np.sin(np.radians(phi))])
        mic = r * np.array([np.cos(thr), np.sin(thr)])
        return np.linalg.norm(mic - img) - r

    Dobs = np.array([combs[p]["D"] for p in poss])
    amp = np.array([combs[p]["a"] for p in poss])
    fits = []
    for r in [0.6, 0.8, 1.0, 1.2, 1.5]:
        best = None
        for d in np.arange(0.3, 3.0, 0.02):
            for phi in np.arange(-180, 180, 2):
                Dm = np.array([plane_D(r, d, phi, th) for th in poss])
                rss = np.sum(amp * (Dm - Dobs) ** 2) / np.sum(amp)
                if best is None or rss < best[0]:
                    best = (rss, d, phi, Dm)
        fits.append(dict(r=r, d=float(best[1]), phi=float(best[2]), rms=float(np.sqrt(best[0])), Dmodel=best[3].tolist()))
    report["plane_fits"] = fits
    print("\nImage-source plane fit to the per-position extra path (weighted by echo amplitude):")
    for ft in fits:
        print(f"  r={ft['r']:.1f} m -> plane at d={ft['d']:.2f} m, normal toward {ft['phi']:+.0f} deg, rms(D) {ft['rms']:.2f} m")

    with open(os.path.join(a.out, "remedies-diagnostics.json"), "w") as fh:
        json.dump(report, fh, indent=1)

    # ---- figures
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(1, 2, figsize=(15, 5.2), gridspec_kw=dict(width_ratios=[1.6, 1]))
        im = ax[0].imshow(Pp, aspect="auto", cmap="RdBu_r", vmin=-6, vmax=6, origin="lower")
        ax[0].set_yticks(range(len(poss)))
        ax[0].set_yticklabels([f"{p:+.0f}°" for p in poss])
        ax[0].set_xticks(range(len(keys)))
        ax[0].set_xticklabels([f"{probe[k]['f']:.0f}" for k in keys], rotation=90, fontsize=7)
        ax[0].set_title(f"Tones only: room term at each BPF harmonic ({len(tone_pwms)} PWM steps × {NH} harmonics), dB from a circle", fontsize=10)
        ax[0].set_xlabel("probe frequency, Hz (harmonic h of the BPF at each PWM step)")
        for i in range(len(poss)):
            for j in range(len(keys)):
                ax[0].text(j, i, f"{Pp[i, j]:+.1f}", ha="center", va="center", fontsize=5.5, color="k" if abs(Pp[i, j]) < 3 else "w")
        im2 = ax[1].imshow(Pb_all, aspect="auto", cmap="RdBu_r", vmin=-6, vmax=6, origin="lower")
        ax[1].set_yticks(range(len(poss)))
        ax[1].set_yticklabels([f"{p:+.0f}°" for p in poss])
        ax[1].set_xticks(range(len(THIRD_OCT)))
        ax[1].set_xticklabels([f"{fc:.0f}" for fc in THIRD_OCT], rotation=90, fontsize=7)
        ax[1].set_title(f"Broadband only (tones and shaft harmonics notched), third-octave, all {len(caps)} captures", fontsize=10)
        ax[1].set_xlabel("third-octave centre, Hz")
        for i in range(len(poss)):
            for j in range(len(THIRD_OCT)):
                ax[1].text(j, i, f"{Pb_all[i, j]:+.1f}", ha="center", va="center", fontsize=5.5, color="k" if abs(Pb_all[i, j]) < 3 else "w")
        plt.colorbar(im2, ax=ax[1], label="dB")
        plt.tight_layout()
        plt.savefig(os.path.join(a.out, "remedies-fig-tones-vs-broadband.png"), dpi=120)
        plt.close()

        fig, axs = plt.subplots(4, 3, figsize=(13, 10), sharex=True, sharey=True)
        ff = np.linspace(120, 1700, 800)
        for i, p in enumerate(poss):
            axx = axs.flat[i]
            c = combs[p]
            axx.errorbar(Fp, Pp[i], yerr=SEp[i], fmt="o", ms=3, color="#96382a", lw=0.8)
            model = 20 * np.log10(np.abs(1 + c["a"] * np.exp(-2j * np.pi * ff * c["D"] / C_SOUND))) + c["c0"]
            axx.plot(ff, model, color="#17566e", lw=1.2)
            axx.axhline(0, color="k", lw=0.5)
            axx.set_title(f"{p:+.0f}°: best single echo D={c['D']:.2f} m, a={c['a']:.2f}, rms {c['rms0']:.1f}→{c['rms']:.1f} dB", fontsize=8.5)
            axx.set_xscale("log")
            axx.set_xlim(130, 1700)
            axx.set_ylim(-10, 8)
        axs.flat[-1].axis("off")
        for axx in axs[-1]:
            axx.set_xlabel("probe frequency, Hz")
        for axx in axs[:, 0]:
            axx.set_ylabel("dB from a circle")
        fig.suptitle("The tone as a swept probe: room term at each BPF harmonic across the PWM steps (dots, ±1 s.e.), with the best single-echo comb per position (line)", fontsize=10)
        plt.tight_layout()
        plt.savefig(os.path.join(a.out, "remedies-fig-probe-comb.png"), dpi=120)
        plt.close()

        fig, axx = plt.subplots(figsize=(11, 4.5))
        for s, arr in fig_cep.items():
            pos = [(-m["elev"] if cp["run"] in rot else m["elev"]) for cp in caps for m in cp["mics"] if m["serial"] == s]
            lab = f"{s} ({np.median(pos):+.0f}°)" if pos else s
            sel = (q > 0.3e-3) & (q < 12e-3)
            axx.plot(q[sel] * 1e3, arr[sel], lw=0.9, label=lab)
        axx.set_xlabel("quefrency, ms (extra path = 0.343 m per ms)")
        axx.set_ylabel("cepstrum amplitude")
        axx.legend(fontsize=7, ncol=3)
        axx.set_title("Cepstrum of the tone-notched broadband ripple, 300 Hz – 6 kHz, mean over tone captures, per microphone", fontsize=10)
        plt.tight_layout()
        plt.savefig(os.path.join(a.out, "remedies-fig-cepstrum.png"), dpi=120)
        plt.close()

        fig, axs = plt.subplots(1, 2, figsize=(12, 3.8))
        cols = ["#17566e", "#96382a", "#8f5c0d"]
        for k, p in enumerate(tone_pwms):
            pr_ = probe[(p, 1)]
            axs[0].errorbar(poss, pr_["P"], yerr=pr_["se"], fmt="o-", ms=3, lw=1.1, color=cols[k % 3], label=f"BPF {pr_['f']:.0f} Hz (PWM {p}, {pr_['n']} runs)")
            axs[1].errorbar(poss, pr_["Pl"], yerr=pr_["sel"], fmt="s--", ms=3, lw=1.1, color=cols[k % 3], label=f"broadband 7–15 Hz beside {pr_['f']:.0f} Hz")
        for axx in axs:
            axx.axhline(0, color="k", lw=0.5)
            axx.set_xticks(poss)
            axx.set_xticklabels([f"{p:+.0f}" for p in poss], fontsize=7)
            axx.set_xlabel("position on the arc, °")
            axx.legend(fontsize=7)
            axx.set_ylim(-10, 9)
        axs[0].set_ylabel("dB from a circle")
        axs[0].set_title("The blade tone at three motor speeds", fontsize=10)
        axs[1].set_title("The broadband floor right beside the tone, same captures", fontsize=10)
        plt.tight_layout()
        plt.savefig(os.path.join(a.out, "remedies-fig-three-speeds.png"), dpi=120)
        plt.close()

        rows1 = [d for d in disc if d["h"] == 1]
        fig, axs = plt.subplots(1, len(rows1), figsize=(3.4 * len(rows1), 3.6), sharey=True)
        for k, row in enumerate(rows1):
            axx = axs[k] if len(rows1) > 1 else axs
            axx.errorbar(poss, row["tone"], yerr=row["tone_se"], fmt="o-", color="#96382a", ms=3, lw=1, label="BPF tone")
            axx.errorbar(poss, row["bb"], yerr=row["bb_se"], fmt="s--", color="#17566e", ms=3, lw=1, label="broadband, same band")
            axx.axhline(0, color="k", lw=0.5)
            axx.set_title(f"PWM {row['pwm']}: BPF {row['f']:.0f} Hz, band {row['band']:.0f} Hz", fontsize=9)
            axx.set_xlabel("position, °")
            axx.set_xticks([-90, -54, -18, 18, 54, 90])
        (axs[0] if len(rows1) > 1 else axs).set_ylabel("dB from a circle")
        (axs[0] if len(rows1) > 1 else axs).legend(fontsize=7)
        plt.tight_layout()
        plt.savefig(os.path.join(a.out, "remedies-fig-bpf-tone-vs-broadband.png"), dpi=120)
        plt.close()
    except ImportError:
        pass


if __name__ == "__main__":
    main()
