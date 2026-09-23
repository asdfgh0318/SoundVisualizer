"""A small isometric picture of the rig: the room, the tripod, the sphere, the arc."""
import numpy as np

INK, MID, MUT = "#14181d", "#4b5563", "#9aa3ab"
ORANGE, ROOM = "#c25e00", "#c8cdd4"

def _p(x, y, z):
    """Axonometric projection — x to the lower-right, y to the lower-left, z up."""
    c, s = np.cos(np.deg2rad(28)), np.sin(np.deg2rad(28))
    return (x - y) * c, (x + y) * s + z

def rig_icon(ax, *, vertical, plus90_up=True, driver=None, R=0.40, zc=0.56):
    ax.set_axis_off(); ax.set_aspect("equal")
    ax.set_xlim(-1.55, 1.55); ax.set_ylim(-0.85, 1.95)

    # --- the room, as a box: floor drawn solid, the two back walls as edges
    fx, fy = 0.82, 0.82
    floor = [(-fx, -fy, 0), (fx, -fy, 0), (fx, fy, 0), (-fx, fy, 0)]
    P = [_p(*v) for v in floor]
    ax.fill([p[0] for p in P], [p[1] for p in P], color="#f4f6f8", zorder=0)
    ax.plot([p[0] for p in P] + [P[0][0]], [p[1] for p in P] + [P[0][1]],
            color=ROOM, lw=0.8, zorder=1)
    H = 0.98
    for corner in ((-fx, -fy), (fx, -fy), (-fx, fy)):
        a, b = _p(*corner, 0), _p(*corner, H)
        ax.plot([a[0], b[0]], [a[1], b[1]], color=ROOM, lw=0.8, zorder=1)
    top_back = [(-fx, -fy, H), (fx, -fy, H), (fx, fy, H)]
    Q = [_p(*v) for v in top_back]
    ax.plot([q[0] for q in Q], [q[1] for q in Q], color=ROOM, lw=0.8, zorder=1)
    Q2 = [_p(-fx, -fy, H), _p(-fx, fy, H)]
    ax.plot([q[0] for q in Q2], [q[1] for q in Q2], color=ROOM, lw=0.8, zorder=1)

    # --- tripod: three legs from the floor up to the sphere
    for a in (90, 210, 330):
        r = 0.30
        foot = _p(r*np.cos(np.deg2rad(a)), r*np.sin(np.deg2rad(a)), 0)
        top = _p(0, 0, zc - 0.07)
        ax.plot([foot[0], top[0]], [foot[1], top[1]], color=MID, lw=1.0,
                solid_capstyle="round", zorder=3)

    # --- the arc of capsules
    t = np.linspace(-np.pi/2, np.pi/2, 160)
    if vertical:
        pts = [(0.0, R*np.cos(u), zc + R*np.sin(u)) for u in t]
        ends = {True: (0.0, 0.0, zc + R), False: (0.0, 0.0, zc - R)}
        axis = (0.85, 0.0, 0.0)                      # fires along the ring axis
    else:
        pts = [(R*np.sin(u), R*np.cos(u), zc) for u in t]
        ends = {True: (0.0, R, zc), False: (0.0, -R, zc)}
        axis = (0.0, 0.0, 0.62)
    XY = np.array([_p(*v) for v in pts])
    ax.plot(XY[:, 0], XY[:, 1], color=MID, lw=1.1, solid_capstyle="round", zorder=4)
    e = np.linspace(-np.pi/2, np.pi/2, 11)
    caps = ([(0.0, R*np.cos(u), zc + R*np.sin(u)) for u in e] if vertical
            else [(R*np.sin(u), R*np.cos(u), zc) for u in e])
    C = np.array([_p(*v) for v in caps])
    ax.scatter(C[:, 0], C[:, 1], s=5.5, color=INK, zorder=5, linewidths=0)
    ex, ey = _p(*ends[plus90_up])
    ax.scatter([ex], [ey], s=13, marker="s", color=INK, zorder=6, linewidths=0)
    ax.annotate("+90°", (ex, ey), textcoords="offset points",
                xytext=(5, 4 if plus90_up else -7), fontsize=5.0, color=INK,
                ha="left", va="center")

    # --- the sphere and the direction it fires
    sx, sy = _p(0, 0, zc)
    ax.scatter([sx], [sy], s=34, color=ORANGE, zorder=7, linewidths=0)
    ax_end = _p(*axis[:2], zc + axis[2]) if not vertical else _p(axis[0], 0, zc)
    ax.annotate("", xy=ax_end, xytext=(sx, sy),
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.0,
                                mutation_scale=5, shrinkA=2.5, shrinkB=0), zorder=7)
    if driver is not None:                 # a tick on the sphere = the driver's roll
        a = np.deg2rad(driver)
        p0 = _p(0.0, 0.05*np.sin(a), zc + 0.05*np.cos(a))
        p1 = _p(0.0, 0.26*np.sin(a), zc + 0.26*np.cos(a))
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color="#7a3a00", lw=1.8,
                solid_capstyle="round", zorder=8)
