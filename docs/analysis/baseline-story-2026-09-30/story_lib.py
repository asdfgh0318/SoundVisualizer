"""Shared loader for the 2026-09-30 baseline story. Every capture group (one PWM step of one base, all 11 capsules)
is read with a chosen calibration directory, so the same WAVs can be read with the factory or the corrected files.

    from story_lib import groups
    G = groups(base_dir, cal_dir)    # list of dicts: pwm, cid, f0, elev[11], f, mags[11,nf], B[11,19] (tone-notched third-octave dB),
                                     #                T[11,6] (BPF harmonic dB), ff, magf[11,nff] (fine spectrum)
"""
import glob, json, os, sys, importlib.util
import numpy as np
from scipy.io import wavfile
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, ROOT)
from server.core import calibration as C
from server.core.fft import compute_fft
_s = importlib.util.spec_from_file_location('avd', os.path.join(ROOT, 'scripts', 'arc_validation_diagnostics.py'))
avd = importlib.util.module_from_spec(_s); _s.loader.exec_module(avd)
FC = np.array(avd.THIRD_OCT)


def cals(cal_dir):
    out = {}
    for t in glob.glob(os.path.join(cal_dir, '*.txt')):
        with open(t) as fh:
            out[os.path.basename(t)[:-4]] = C.parse_umik_calibration(fh.read())
    return out


def groups(base_dir, cal_dir, fine=False):
    cs = cals(cal_dir)
    by = {}
    for p in sorted(glob.glob(os.path.join(base_dir, 'measurements', '*acoustic*'))):
        m = json.load(open(os.path.join(p, 'meta.json')))
        cid = os.path.basename(p).split('__')[0]
        by.setdefault((m['pwm_setpoint'], cid), []).append((m, p))
    out = []
    for (pwm, cid), lst in sorted(by.items(), key=lambda kv: kv[0][1]):
        if len(lst) != 11:
            continue
        lst.sort(key=lambda mp: -float(mp[0]['elevation_deg']))
        mags, fm, mf = [], [], []
        for m, p in lst:
            fs, x = avd.read_wav(os.path.join(p, 'audio.wav'))
            cal = cs.get(m['calibration_file_id'])
            f, mag = avd.spectrum(x, fs, cal); mags.append(mag)
            if fine:
                ff, mg = compute_fft(x, fs, size=16384)
                mf.append(C.apply_calibration_to_spectrum(ff, mg, cal) if cal is not None else mg)
        mags = np.array(mags)
        f0, ok = avd.find_bpf(f, mags) if pwm >= 1800 else (None, False)
        method = 'harmonics 1-3' if ok else None
        if pwm >= 1800 and not ok:                 # fallback: 3xBPF dominates this source (Sept flat runs too); f0 = its peak / 3
            mm = mags.mean(0); sel = (f > 500) & (f < 1000); k = np.where(sel)[0][np.argmax(mm[sel])]
            if mm[k] - np.median(mm[sel]) > 12:
                f0, ok, method = float(f[k]) / 3, True, 'peak of 3xBPF / 3'
        B, T = [], []
        for mg in mags:
            t, b, _ = avd.tone_and_broadband(f, mg, f0 if ok else 150.0)
            B.append(b); T.append(t if ok else np.full(avd.NH, np.nan))
        out.append(dict(pwm=pwm, cid=cid, f0=f0 if ok else None, f0_method=method, elev=np.array([float(m['elevation_deg']) for m, _ in lst]),
                        f=f, mags=mags, B=np.array(B), T=np.array(T), ff=(ff if fine else None), magf=np.array(mf) if fine else None,
                        t_start=lst[0][0]['t_start']))
    return out


def perf(base_dir):
    """median voltage/current/thrust over the second half of each performance log, per pwm (last log wins)"""
    import csv
    out = {}
    for p in sorted(glob.glob(os.path.join(base_dir, 'measurements', '*performance*'))):
        m = json.load(open(os.path.join(p, 'meta.json'))); rows = list(csv.DictReader(open(os.path.join(p, 'telemetry.csv'))))
        if not rows: continue
        c = lambda k: float(np.median([float(r[k]) for r in rows[len(rows) // 2:]]))
        out[m['pwm_setpoint']] = dict(V=c('voltage_v'), I=c('current_a'), T=c('thrust_n'))
    return out
