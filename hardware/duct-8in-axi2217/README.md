# Pusher duct for the APC 8x4.5MRP on the AXI 2217/12 (r27 tree)

A parametric duct designed to the rules in
[`docs/acoustic-speculations/duct-inlet-design-rules.pdf`](../../docs/acoustic-speculations/duct-inlet-design-rules.pdf).
The present r27 duct, unlined, gives −8.01 N at 2000 µs against −10.57 N for the bare
propeller (2026-11-02), so it costs thrust. This one is meant to add it. **Untested: nothing
here has been printed or run yet.**

**Pusher layout (2026-11-02, Adam's choice):** the first duct's shape, with the motor moved to
the inlet side. Air enters through the lip past the Tyto motor plate, the spider and the motor,
goes through the propeller and leaves through the diffuser. The spider sits 20 mm above the lip:
a hub on the motor's rear face and three plain box arms that reach past the lip and drop as legs
down the outside of the duct, each held by one radial M3 screw into a heat-set insert in the
outer wall. Nothing crosses the outlet and the inside of the duct stays smooth. It needs a pusher
propeller (APC 8x4.5MRP) or the motor reversed with the propeller flipped, and the stand will
read thrust with the opposite sign to a tractor set-up.

![half-section](section.png)

| | value | rule it comes from |
|---|---|---|
| tip gap | 1.0 mm (throat Ø205.2) | 1: as small as can be built |
| inlet lip radius | 25 mm = 12.2 % D<sub>t</sub> | 2: 10–13 % D<sub>t</sub>, never under ~6 % |
| wall at the propeller plane | 30 mm (outer Ø265.2) | 3: ≥ 10 % of D = 20.3 mm |
| propeller disc | 35 mm below the lip edge, 39 % of the length | 4: behind the lip (NASA: 45 %) |
| diffuser | 10°, 45 mm, exit Ø221.1, exit/disc area 1.18 | 5: 10°, area ratio 1.1–1.3 |
| spider | hub + 3 box arms (8 × 12 mm) 20 mm above the lip, legs down the outer wall | 6: supports out of the rotor plane (55 mm upstream of the disc) |
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
  `prop_to_mount` moves the spider; the model refuses (assert) if the motor face would end up
  inside the lip.
- `duct_quarter.stl` — print **4×** (133 × 133 × 90 mm, exit face on the bed); 4 pin holes
  Ø3.2 per cut face for 3 mm pins or filament offcuts, then glue. Three of the quarters' outer
  walls carry an M3 heat-set insert for a spider leg.
- `duct_full.stl` — the whole ring, for a bed of at least 270 mm.
- `spider.stl` — hub + 3 arms + legs (238 × 238 × 60 mm), exported arms-down so it prints with
  no supports; needs a bed of at least 240 mm. The motor bolts to its downstream face and the
  Tyto motor plate to its upstream face, on the same long M3 bolts (stand plate → spider → motor).
- `viewer.html` — interactive 3D view in the browser (three.js from the CDN; built from the same
  numbers as `duct.scad`, so keep the two in step). Open it with `/snap/bin/brave viewer.html`.
- `render.py` — redraws `section.png`, `assembly.png` and `spider-hub.png` (OpenSCAD's own PNG export needs a display).

## Measure before printing

The motor dimensions in `duct.scad` are **placeholders, not verified data** (marked `[MEASURE]`):

- `prop_to_mount` (55 mm) — propeller disc to the motor's rear mounting face, with the prop adapter fitted;
- `hub_hole_d` (9 mm) — clearance for the shaft end and circlip at the motor's rear.

The rear-mount holes are **not** a placeholder: 4 × M3 in a cross, one pair 19 mm apart and the
other 16 mm apart, from AXI's own drawing ("AXI 2208 & 2212 & 2217", catalogue
`modelmotors.cz/file/wisiwig/files/actual_katalog_lr.pdf`, p. 6; body Ø27.7 × 35 mm for the
2217). Check them against your motor anyway — the drawing covers the V1 Gold Line series. The
Tyto motor plate must take the same pattern (`spider-hub.png` shows the hub's holes).
- `throat_len` (20 mm) — straight throat around the disc; must cover the blade tips' axial extent.

Measure the real tip gap after assembly with a feeler gauge. A ring printed in four pieces will
not be round to 0.1 mm, so sand the throat until the tightest blade clears everywhere.

## Testing it

Same-day bare propeller and current unlined duct first, then this duct, then the bare propeller
again (§05 of the rules PDF). Repeats of one set-up agree within 0.1 N, so a difference above
~0.2 N is real. Compare per watt or at equal rpm as well as at equal ESC signal, and mind the
flipped thrust sign.
