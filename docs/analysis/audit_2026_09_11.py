#!/usr/bin/env python3
"""Recompute every figure our documents assert from our own data, and check each one.

    python docs/analysis/audit_2026_09_11.py

Claimed values are those printed in docs/arc-validation-onepager.pdf,
docs/arc-validation-remedies.pdf, docs/chamber-fighting-guide.pdf and CLAUDE.md
on 2026-09-11. A FAIL means a document and the data disagree; fix the document.
"""
import csv
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
C = 343.0
PASSED: list = []
FAILED: list = []


def chk(name, claimed, actual, tol, unit=""):
    (PASSED if abs(claimed - actual) <= tol else FAILED).append((name, claimed, actual, unit))
    print(f"{'PASS' if abs(claimed-actual)<=tol else 'FAIL'}  {name:<58} "
          f"claimed {claimed:>8} | recomputed {actual:>8.3f} {unit}")


def load(p):
    with open(os.path.join(HERE, p)) as fh:
        r = list(csv.reader(fh))
    f = np.array([float(h.replace("Hz", "")) for h in r[0][1:]])
    pos = np.array([float(x[0]) for x in r[1:]])
    return f, pos, np.array([[float(v) for v in x[1:]] for x in r[1:]])


def main():
    print("=== A. Broadband position map ===")
    f, pos, B = load("remedies-broadband-position-map-allpwm.csv")
    _, _, SE = load("remedies-broadband-position-se-allpwm.csv")
    chk("broadband cells within +-1.3 dB (%)", 92, np.mean(np.abs(B) <= 1.3) * 100, 0.6, "%")
    chk("worst broadband cell (dB)", 2.7, np.abs(B).max(), 0.05, "dB")
    chk("cells beyond 3 s.e.", 99, (np.abs(B) / SE > 3).sum(), 0)
    chk("total cells", 209, B.size, 0)
    chk("within 1.3 dB below 3.15 kHz (%)", 92.2, np.mean(np.abs(B[:, f < 3000]) <= 1.3) * 100, 0.1, "%")
    chk("within 1.3 dB at/above 3.15 kHz (%)", 92.7, np.mean(np.abs(B[:, f >= 3000]) <= 1.3) * 100, 0.1, "%")
    chk("worst cell below 3.15 kHz (dB)", 2.69, np.abs(B[:, f < 3000]).max(), 0.01, "dB")
    chk("worst cell at/above 3.15 kHz (dB)", 2.58, np.abs(B[:, f >= 3000]).max(), 0.01, "dB")

    print("\n=== B. Largest within-group contrasts (the degeneracy argument) ===")
    groups = [(-90, 90), (-72, -54, 54, 72), (-36, 36), (-18, 18), (0,)]

    def best_within(M, freqs, positions):
        idx = {p: i for i, p in enumerate(positions)}
        out = (0.0, None, None, None)
        for g in groups:
            for i, a in enumerate(g):
                for b in g[i + 1:]:
                    for k, fc in enumerate(freqs):
                        d = abs(M[idx[a], k] - M[idx[b], k])
                        if d > out[0]:
                            out = (d, a, b, fc)
        return out

    d, _, _, fc = best_within(B, f, pos)
    chk("largest broadband within-group contrast (dB)", 4.3, d, 0.05, f"dB at {fc:.0f} Hz")
    ft, pt, T = load("arc-error-map-third-octave.csv")
    d2, _, _, fc2 = best_within(T, ft, pt)
    chk("largest mixed-band within-group contrast (dB)", 12.5, d2, 0.05, f"dB at {fc2:.0f} Hz")

    print("\n=== C. ISO 3745 tolerance as an analogy ===")
    def tol(fq):
        return 1.5 if fq <= 630 else (1.0 if fq < 6300 else 1.5)
    chk("broadband cells outside tolerance", 29,
        sum(int((np.abs(B[:, i]) > tol(f[i])).sum()) for i in range(len(f))), 0, "of 209")
    chk("mixed-band cells outside tolerance", 55,
        sum(int((np.abs(T[:, i]) > tol(ft[i])).sum()) for i in range(len(ft))), 0, "of 209")

    print("\n=== D. Microphone terms ===")
    with open(os.path.join(HERE, "remedies-mic-offsets-pwm1900.csv")) as fh:
        r = list(csv.reader(fh))
    Mv = np.array([[float(v) for v in x[1:]] for x in r[1:]])
    chk("mic terms minimum (dB)", -5.8, Mv.min(), 0.05, "dB")
    chk("mic terms maximum (dB)", 3.0, Mv.max(), 0.05, "dB")

    print("\n=== E. Echo delays and the gating limit ===")
    for extra, ms, hz in ((0.68, 1.98, 500), (1.49, 4.34, 230)):
        chk(f"delay for {extra} m (ms)", ms, extra / C * 1000, 0.01, "ms")
        chk(f"1/T limit for {extra} m (Hz)", hz, 1 / (extra / C), 5, "Hz")
    chk("extra path to gate at 250 Hz (m)", 1.37, C / 250, 0.01, "m")

    print("\n=== F. Fit identifiability ===")
    with open(os.path.join(HERE, "arc-validation-data.json")) as fh:
        d_ = json.load(fh)
    runs = sorted([v for v in d_["runs"].values()
                   if any(v["key"].endswith(k) for k in d_["core_runs"])], key=lambda x: x["key"])
    positions, serials = d_["positions"], d_["serials"]
    pi = {p: i for i, p in enumerate(positions)}
    si = {s: i for i, s in enumerate(serials)}
    rows = [(ri, pi[-int(lab) if run["flipped"] else int(lab)], si[run["mics"][lab]["serial"]])
            for ri, run in enumerate(runs) for lab in run["mics"]]
    R, P, S = len(runs), len(positions), len(serials)
    A = np.zeros((len(rows), R + P + S))
    for k, (ri, p, s) in enumerate(rows):
        A[k, ri] = 1
        A[k, R + p] = 1
        A[k, R + P + s] = 1
    chk("parameters per band", 34, A.shape[1], 0)
    chk("observations per band", 132, A.shape[0], 0)
    chk("rank of the design", 28, np.linalg.matrix_rank(A), 0)
    chk("undetermined directions", 6, A.shape[1] - np.linalg.matrix_rank(A), 0)
    chk("undetermined directions if M known", 1,
        (R + P) - np.linalg.matrix_rank(A[:, :R + P]), 0)
    parent = list(range(P + S))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for _, p, s in rows:
        ra, rb = find(p), find(P + s)
        if ra != rb:
            parent[ra] = rb
    chk("connected position/serial groups", 5, len({find(i) for i in range(P + S)}), 0)

    print("\n=== G. The degeneracy check at 794 Hz ===")
    i794 = int(np.argmin(abs(f - 794)))
    obs = np.array([float(run["mics"][lab]["cal"][i794]) for run in runs for lab in run["mics"]])
    Ac = np.vstack([A,
                    np.r_[np.zeros(R), 50 * np.ones(P), np.zeros(S)],
                    np.r_[np.zeros(R + P), 50 * np.ones(S)]])
    x = np.linalg.pinv(Ac) @ np.r_[obs, 0, 0]
    chk("residual RMS at 794 Hz (dB)", 1.5012, math.sqrt(((obs - A @ x) ** 2).mean()), 0.0005, "dB")
    x2 = x.copy()
    for i in (pi[-36.0], pi[36.0]):
        x2[R + i] += 1.0
    for j in (si["8108893"], si["8108900"]):
        x2[R + P + j] -= 1.0
    chk("residual RMS after the 1 dB group shift (dB)", 1.5012,
        math.sqrt(((obs - A @ x2) ** 2).mean()), 0.0005, "dB")

    print("\n=== H. Hub source design (Visaton FRS 8 M datasheet parameters) ===")
    fs, qts, sd = 125.0, 0.49, 29e-4
    ratio = 1.1 / 1.0  # Vas / Vb, box volume 1.0 litre
    fc_box, qtc = fs * math.sqrt(ratio + 1), qts * math.sqrt(ratio + 1)
    chk("sealed 1 l Fc (Hz)", 181, fc_box, 0.5, "Hz")
    chk("sealed 1 l Qtc", 0.71, qtc, 0.005)

    def hp(fq):
        x_ = (fq / fc_box) ** 2
        return 20 * math.log10(x_ / math.sqrt((1 - x_) ** 2 + x_ / qtc ** 2))

    for fq, claim in ((216, -1.7), (238, -1.2), (258, -0.9), (125, -7.3)):
        chk(f"box response at {fq} Hz (dB)", claim, hp(fq), 0.05, "dB")
    chk("effective piston diameter (cm)", 6.1, 2 * math.sqrt(sd / math.pi) * 100, 0.05, "cm")
    chk("ka=1 omni limit (Hz)", 1800, C / (math.pi * 2 * math.sqrt(sd / math.pi)), 20, "Hz")
    chk("decay to -20 dB (ms)", 2.9, 2.303 * qtc / (math.pi * fc_box) * 1000, 0.05, "ms")
    chk("decay to -30 dB (ms)", 4.3, 3.454 * qtc / (math.pi * fc_box) * 1000, 0.05, "ms")

    print("\n=== I. Propeller levels at the microphones (prop18, PWM 1900) ===")
    rr = next(v for v in d_["runs"].values() if v["key"].endswith("prop18"))
    arr = np.array([[float(v) for v in m["cal"][:19]] for m in rr["mics"].values()])
    chk("lowest band mean (dB)", 24, arr.mean(axis=0).min(), 1.0, "dB")
    chk("highest band mean (dB)", 62, arr.mean(axis=0).max(), 1.0, "dB")
    chk("overall 100 Hz-10 kHz mean (dB)", 67,
        float(np.mean([float(m["cal"][19]) for m in rr["mics"].values()])), 0.5, "dB")

    print(f"\n{'=' * 70}\nAUDIT RESULT: {len(PASSED)} passed, {len(FAILED)} failed")
    for n, cl, ac, u in FAILED:
        print(f"  FAILED: {n}: document says {cl}, recomputed {ac:.3f} {u}")
    return 1 if FAILED else 0


if __name__ == "__main__":
    raise SystemExit(main())
