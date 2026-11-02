"""Previews for the pusher duct (motor upstream, spider over the inlet): a dimensioned half-section and a 3D view of the exported STLs.

OpenSCAD's PNG export needs a display; this draws from the same numbers instead.
Keep the parameters below in step with duct.scad.
"""
import math
import re
import struct
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

prop_d, tip_gap, throat_len = 203.2, 1.0, 20
lip_r, lip_out_r, wall = 25, 5, 30
prop_to_mount, diff_angle, diff_len = 55, 10, 45
hub_r, arm_t, leg_t, leg_bolt_z = 22, 12, 7, 70
throat_r = prop_d / 2 + tip_gap
exit_r = throat_r + diff_len * math.tan(math.radians(diff_angle))
outer_exit_r = exit_r + 14.5
outer_r = throat_r + wall
z_prop = diff_len + throat_len / 2
z_lip0 = diff_len + throat_len
z_top = z_lip0 + lip_r
z_mount = z_prop + prop_to_mount
leg_r0 = outer_r + 0.3
hl = throat_r + lip_r


def arc(c, r, a0, a1, n=30):
    return [(c[0] + r * math.cos(math.radians(a)), c[1] + r * math.sin(math.radians(a))) for a in np.linspace(a0, a1, n)]


prof = [(exit_r, 0), (throat_r, diff_len), (throat_r, z_lip0)] + arc((hl, z_lip0), lip_r, 180, 90) \
    + arc((hl, z_top - lip_out_r), lip_out_r, 90, 0) + [(outer_r, z_prop), (outer_exit_r, 0)]


def section(path):
    fig, ax = plt.subplots(figsize=(11, 7.6))
    r, z = zip(*prof)
    ax.fill(r, z, color="#4a7fa8", alpha=.85, lw=1, ec="#17364a")
    ax.plot([0, prop_d / 2], [z_prop, z_prop], color="#d9822b", lw=3, label="APC 8x4.5MRP disc (pusher)")
    ax.add_patch(plt.Rectangle((0, z_mount - 35), 27.7 / 2, 35, color="#999", alpha=.7, label="AXI 2217 body, Ø27.7 × 35 (AXI catalogue)"))
    ax.add_patch(plt.Rectangle((0, z_mount), leg_r0 + leg_t, arm_t, color="#555", alpha=.8, label="spider: hub + 3 box arms + legs"))
    ax.add_patch(plt.Rectangle((leg_r0, leg_bolt_z - 8), leg_t, z_mount - (leg_bolt_z - 8), color="#555", alpha=.8))
    ax.plot([leg_r0 - 9, leg_r0 + leg_t], [leg_bolt_z, leg_bolt_z], color="k", lw=1.2)
    ax.add_patch(plt.Rectangle((0, z_mount + arm_t), 20, 4, color="#333", alpha=.5, label="Tyto motor plate (placeholder)"))
    ax.annotate("", xy=(60, z_top + 5), xytext=(60, z_top + 45), arrowprops=dict(arrowstyle="-|>", color="k"))
    ax.text(63, z_top + 30, "air in", fontsize=9)
    ax.annotate("", xy=(60, -22), xytext=(60, 3), arrowprops=dict(arrowstyle="-|>", color="k"))
    ax.text(63, -14, "air out", fontsize=9)
    ax.axvline(0, color="k", lw=.6, ls="-.")
    notes = [
        ((throat_r - 0.5, z_prop - 2), f"tip gap {tip_gap:.1f} mm\nthroat Ø{2 * throat_r:.1f}", (20, z_prop - 30)),
        ((hl - lip_r * .7, z_lip0 + lip_r * .72), f"lip radius {lip_r} mm ({100 * lip_r / (2 * throat_r):.1f} % Dt)", (40, z_top - 8)),
        ((outer_r - 10, z_prop), f"wall {wall} mm (≥ 20.3)\nouter Ø{2 * outer_r:.1f}", (160, z_prop + 20)),
        (((exit_r + throat_r) / 2, diff_len / 2), f"diffuser {diff_angle}°, {diff_len} mm\nexit Ø{2 * exit_r:.1f}, area ratio {(exit_r / (prop_d / 2)) ** 2:.2f}", (150, 5)),
        ((leg_r0 + leg_t, leg_bolt_z), "leg: one M3 screw into a\nheat-set insert in the wall", (150, leg_bolt_z - 40)),
    ]
    for xy, txt, xt in notes:
        ax.annotate(txt, xy=xy, xytext=xt, fontsize=8.5, arrowprops=dict(arrowstyle="->", lw=.7))
    ax.text(110, -38, f"length {z_top:.0f} mm; disc {z_top - z_prop:.0f} mm below the lip edge ({100 * (z_top - z_prop) / z_top:.0f} % of the length)", fontsize=8.5)
    ax.set_aspect("equal")
    ax.set_xlim(-5, 230)
    ax.set_ylim(-45, z_mount + 30)
    ax.set_xlabel("radius from the axis, mm")
    ax.set_ylabel("height above the exit face, mm")
    ax.set_title("Pusher duct for APC 8x4.5MRP on AXI 2217/12 — half-section (axis on the left)", fontsize=10)
    ax.legend(loc="lower left", bbox_to_anchor=(0.0, 0.08), fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=150)


def read_stl(path):
    d = open(path, "rb").read()
    n = struct.unpack("<I", d[80:84])[0]
    if 84 + 50 * n == len(d):
        a = np.frombuffer(d[84:], dtype=np.dtype([("n", "<3f4"), ("v", "<9f4"), ("a", "<u2")]), count=n)
        return a["v"].reshape(-1, 3, 3).astype(float)
    v = np.array([list(map(float, m.groups())) for m in re.finditer(rb"vertex\s+(\S+)\s+(\S+)\s+(\S+)", d)])
    return v.reshape(-1, 3, 3)


def view3d(path, parts):
    fig = plt.figure(figsize=(9, 8.5))
    ax = fig.add_subplot(projection="3d")
    light = np.array([0.4, -0.5, 0.75]); light /= np.linalg.norm(light)
    for f, col, cut, flip_at in parts:
        t = read_stl(f)
        if flip_at is not None:                           # spider.stl is exported upside down for printing
            t[:, :, 2] = flip_at - t[:, :, 2]
            t[:, :, 1] = -t[:, :, 1]
        if cut:
            t = t[(t[:, :, 1] >= -1).all(axis=1)]         # cut away the half nearest the camera to show the inside
        nrm = np.cross(t[:, 1] - t[:, 0], t[:, 2] - t[:, 0])
        nrm /= np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-12
        shade = 0.35 + 0.65 * np.clip(nrm @ light, 0, 1)
        base = np.array(matplotlib.colors.to_rgb(col))
        ax.add_collection3d(Poly3DCollection(t, facecolors=np.clip(base[None] * shade[:, None], 0, 1), edgecolors="none"))
    ax.set_xlim(-140, 140); ax.set_ylim(-140, 140); ax.set_zlim(-10, 140)
    ax.set_box_aspect((280, 280, 150))
    ax.view_init(elev=24, azim=-60)
    ax.set_axis_off()
    ax.set_title("Pusher duct (half cut away) with the motor spider; air enters at the top", fontsize=10)
    fig.tight_layout()
    fig.savefig(path, dpi=130)


if __name__ == "__main__":
    section("section.png")
    view3d("assembly.png", [("duct_full.stl", "#4a7fa8", True, None), ("spider.stl", "#555555", False, z_mount + arm_t)])
    print("wrote section.png, assembly.png", file=sys.stderr)


def spider_top(path):
    """Top view of spider.stl, to check the motor holes are cut."""
    t = read_stl("spider.stl")
    fig, ax = plt.subplots(figsize=(6, 6))
    top = t[(np.abs(t[:, :, 2] - t[:, :, 2].min()) < 1e-3).all(axis=1)]      # the flat face on the bed
    for tri in top:
        ax.fill(tri[:, 0], tri[:, 1], color="#555", lw=0)
    for x, y, lab in [(9.5, 0, "M3, 19 mm pair"), (0, 8, "M3, 16 mm pair")]:
        ax.annotate(lab, xy=(x, y), xytext=(x + 25, y + 30), fontsize=8, arrowprops=dict(arrowstyle="->", lw=.7))
    ax.set_aspect("equal"); ax.set_xlim(-40, 40); ax.set_ylim(-40, 40)
    ax.set_title("Spider hub, bed face: AXI 2217 rear mount (4 × M3, 19 / 16 mm) + Ø9 centre", fontsize=9)
    fig.tight_layout(); fig.savefig(path, dpi=130)


if __name__ == "__main__":
    spider_top("spider-hub.png")
