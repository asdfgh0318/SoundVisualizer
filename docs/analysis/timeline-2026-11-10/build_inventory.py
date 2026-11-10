"""Inventory of every recording in the data repo, in time order.

Reads ../SoundVisualizer-data/data (or $SOUNDVIS_DATA) and writes, next to this file:
  recordings.csv   one row per capture run (prop/motor) or loudspeaker run
  TIMELINE.md      the same, grouped by day

A capture run = measurements of one base whose start times are < 120 s apart.
Telemetry columns are means over the steps at the run's highest ESC signal.
Times are local (Europe/Warsaw).
"""
import csv, json, os, re, sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).parent
DATA = Path(os.environ.get("SOUNDVIS_DATA", HERE / "../../../../SoundVisualizer-data/data")).resolve()
TZ = ZoneInfo("Europe/Warsaw")
GAP_S = 120
TS = re.compile(r"^(\d{4}-\d\d-\d\dT\d\d-\d\d-\d\d-\d+)__(performance|acoustic)")


def parse_ts(s):
    return datetime.strptime(s, "%Y-%m-%dT%H-%M-%S-%f").replace(tzinfo=timezone.utc)


def telemetry_means(path):
    cols = defaultdict(list)
    try:
        with open(path) as f:
            for row in csv.DictReader(f):
                for k in ("thrust_n", "current_a", "voltage_v", "rpm"):
                    cols[k].append(float(row[k]))
    except (OSError, ValueError, KeyError):
        return {}
    return {k: sum(v) / len(v) for k, v in cols.items() if v}


def prop_runs():
    rows = []
    for base in sorted(DATA.iterdir()):
        mdir = base / "measurements"
        if not mdir.is_dir():
            continue
        steps = defaultdict(lambda: {"mics": 0, "perf": None})
        for m in mdir.iterdir():
            g = TS.match(m.name)
            if not g:
                continue
            st = steps[g.group(1)]
            if g.group(2) == "acoustic":
                st["mics"] += 1
            else:
                st["perf"] = m
        times = sorted(steps)
        run = []
        for t in times + [None]:
            if run and (t is None or (parse_ts(t) - parse_ts(run[-1])).total_seconds() > GAP_S):
                rows.append(summarise(base.name, run, steps))
                run = []
            if t:
                run.append(t)
    return rows


def summarise(base, run, steps):
    pwm, rep, tel = {}, {}, {}
    for t in run:
        p = steps[t]["perf"]
        if p is None:
            continue
        try:
            meta = json.loads((p / "meta.json").read_text())
        except (OSError, ValueError):
            continue
        pwm[t] = meta.get("pwm_setpoint")
        rep[t] = meta.get("repeat", 1)
        tel[t] = telemetry_means(p / "telemetry.csv")
    pwms = sorted({v for v in pwm.values() if v is not None})
    top = pwms[-1] if pwms else None
    at_top = [tel[t] for t in run if pwm.get(t) == top and tel.get(t)]

    def mean(k):
        v = [d[k] for d in at_top if k in d]
        return round(sum(v) / len(v), 2) if v else ""

    start = parse_ts(run[0]).astimezone(TZ)
    motor, prop, shroud, notes = (base.split("__") + [""] * 4)[:4]
    return {
        "_ts": frozenset(run),
        "kind": "prop", "date": start.strftime("%Y-%m-%d"), "time": start.strftime("%H:%M"),
        "base": base, "motor": motor, "propeller": prop, "shroud": shroud, "notes": notes,
        "campaign": notes.split("-")[0] if re.match(r"^[a-z]+\d+-", notes) else "",
        "steps": len(run), "mics": max(steps[t]["mics"] for t in run),
        "pwm": " ".join(str(p) for p in pwms), "repeats": max(rep.values(), default=1),
        "top_pwm": top or "", "thrust_n": mean("thrust_n"), "voltage_v": mean("voltage_v"),
        "current_a": mean("current_a"), "rpm_electrical": mean("rpm"),
    }


def merge_copies(rows):
    """A recording kept under two base names (an archive copy made before a redo) is one run.

    Runs that share step timestamps are merged; the row keeps the shortest base name and lists
    the others under also_stored_as.
    """
    groups = []
    for r in sorted(rows, key=lambda r: (len(r["base"]), r["base"])):
        for g in groups:
            if g[0]["_ts"] & r["_ts"]:
                g.append(r)
                break
        else:
            groups.append([r])
    out = []
    for g in groups:
        keep = max(g, key=lambda r: (len(r["_ts"]), -len(r["base"])))
        keep["also_stored_as"] = "; ".join(r["notes"] for r in g if r is not keep)
        out.append(keep)
    return out


def speaker_runs():
    rows = []
    root = DATA / "calibrator-sessions"
    for meta_path in sorted(root.glob("*/*/meta.json")):
        try:
            meta = json.loads(meta_path.read_text())
        except ValueError:
            continue
        day, label = meta_path.parts[-3], meta_path.parts[-2]
        if "timestamp" in meta:  # written in local time
            ts = datetime.fromisoformat(meta["timestamp"])
            date, time = ts.strftime("%Y-%m-%d"), ts.strftime("%H:%M")
        else:  # the two noise-floor runs carry no time
            date, time = day, "--:--"
        freqs = meta.get("freqs") or []
        kind = meta.get("kind") or "single-capsule substitution"
        rows.append({
            "kind": "loudspeaker", "date": date, "time": time,
            "base": f"{day}/{label}", "notes": kind,
            "steps": len(freqs), "mics": len(meta.get("arc") or []) or 1,
            "pwm": f"{min(freqs):.0f}-{max(freqs):.0f} Hz" if freqs else "",
        })
    return rows


FIELDS = ["date", "time", "kind", "campaign", "base", "motor", "propeller", "shroud", "notes", "steps",
          "mics", "pwm", "repeats", "top_pwm", "thrust_n", "voltage_v", "current_a", "rpm_electrical", "also_stored_as"]


def main():
    rows = sorted(merge_copies(prop_runs()) + speaker_runs(), key=lambda r: (r["date"], r["time"], r["base"]))
    with open(HERE / "recordings.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, restval="", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    by_day = defaultdict(list)
    for r in rows:
        by_day[r["date"]].append(r)
    out = ["# Recordings timeline", "",
           f"Built by `build_inventory.py` from the data repo; {len(rows)} runs on {len(by_day)} days. "
           "`recordings.csv` holds the same rows. Times are local. Telemetry is the mean at the run's "
           "highest ESC signal; rpm is electrical as logged.", ""]
    for day in sorted(by_day):
        rs = by_day[day]
        n_prop = sum(r["kind"] == "prop" for r in rs)
        out += [f"## {day}  ({n_prop} prop runs, {len(rs) - n_prop} loudspeaker runs)", "",
                "| Time | Base / run | Mics | Steps | ESC µs or tones | Rep | Thrust N | V | A | rpm el. |",
                "|---|---|---|---|---|---|---|---|---|---|"]
        for r in rs:
            name = (r["base"] + (f" (also: {r['also_stored_as']})" if r.get("also_stored_as") else "")) if r["kind"] == "prop" else f"🔊 {r['base']} ({r['notes']})"
            out.append(f"| {r['time']} | {name} | {r['mics']} | {r['steps']} | {r['pwm']} | {r.get('repeats','')} | "
                       f"{r.get('thrust_n','')} | {r.get('voltage_v','')} | {r.get('current_a','')} | {r.get('rpm_electrical','')} |")
        out.append("")
    (HERE / "TIMELINE.md").write_text("\n".join(out))

    print(f"{len(rows)} runs, {len(by_day)} days, data = {DATA}")
    for day in sorted(by_day):
        rs = by_day[day]
        camp = sorted({r.get("campaign") or ("spk" if r["kind"] != "prop" else "?") for r in rs})
        print(f"{day}  {len(rs):3d} runs  {rs[0]['time']}-{rs[-1]['time']}  {','.join(camp)}")


if __name__ == "__main__":
    main()
