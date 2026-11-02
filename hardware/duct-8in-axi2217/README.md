# Duct for the APC 8x4.5MR on the AXI 2217/12 (r27 tree)

A parametric duct designed to the rules in
[`docs/acoustic-speculations/duct-inlet-design-rules.pdf`](../../docs/acoustic-speculations/duct-inlet-design-rules.pdf).
The present r27 duct, unlined, gives −8.01 N at 2000 µs against −10.57 N for the bare
propeller (2026-11-02), so it costs thrust. This one is meant to add it. **Untested: nothing
here has been printed or run yet.**

![half-section](section.png)

| | value | rule it comes from |
|---|---|---|
| tip gap | 1.0 mm (throat Ø205.2) | 1: as small as can be built |
| inlet lip radius | 25 mm = 12.2 % D<sub>t</sub> | 2: 10–13 % D<sub>t</sub>, never under ~6 % |
| wall at the propeller plane | 30 mm (outer Ø265.2) | 3: ≥ 10 % of D = 20.3 mm |
| propeller disc | 35 mm below the lip, 39 % of the length | 4: behind the lip (NASA: 45 %) |
| diffuser | 10°, 45 mm, exit Ø221.1, exit/disc area 1.18 | 5: 10°, area ratio 1.1–1.3 |
| supports | 3-arm spider at the exit plane, 45 mm behind the disc | 6: ≥ ~11 mm behind the disc; odd arm count so the two blades never pass two arms at once |
| length | 90 mm | |

## Files

The STLs are build output (the repo ignores `*.stl`); regenerate them after any change:

```bash
openscad -D 'part="quarter"' -o duct_quarter.stl duct.scad
openscad -D 'part="duct"'    -o duct_full.stl    duct.scad
openscad -D 'part="spider"'  -o spider.stl       duct.scad
../../.venv/bin/python render.py   # section.png, assembly.png
```

- `duct.scad` — the model; every number above is a parameter at the top. Changing
  `prop_to_mount` moves the exit plane, so the spider always sits on the motor's rear mount.
- `duct_quarter.stl` — print **4×** (133 × 133 × 90 mm, exit face on the bed); 4 pin holes
  Ø3.2 per cut face for 3 mm pins or filament offcuts, then glue.
- `duct_full.stl` — the whole ring, for a bed of at least 270 mm.
- `spider.stl` — motor plate + 3 arms (218 × 191 × 12 mm), printed flat. It sits between the
  motor's rear mount and the Tyto motor plate, and bolts into three M3 heat-set inserts in the
  duct's exit face.
- `render.py` — redraws `section.png` and `assembly.png` (OpenSCAD's own PNG export needs a display).

## Measure before printing

The motor dimensions in `duct.scad` are **placeholders, not verified data** (marked `[MEASURE]`):

- `prop_to_mount` (55 mm) — propeller disc to the motor's rear mounting face, with the prop adapter fitted;
- `mount_holes_n`, `mount_holes_pcd` (4 on Ø25) — the AXI 2217 rear-mount hole pattern;
- `hub_hole_d` (12 mm) — clearance for whatever protrudes from the motor's rear.

Also check that the blade tips' axial thickness fits inside the 20 mm straight throat, and
measure the real tip gap after assembly with a feeler gauge. A 3D-printed ring in four pieces
will not be round to 0.1 mm, so sand the throat until the tightest blade clears everywhere.

## Testing it

Same-day bare propeller and current unlined duct first, then this duct, then the bare propeller
again (§05 of the rules PDF). Repeats of one set-up agree within 0.1 N, so a difference above
~0.2 N is real. Compare per watt or at equal rpm as well as at equal ESC signal.
