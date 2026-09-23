# Hub loudspeaker enclosure — 1 litre sealed sphere

For campaign session 2: a source that sits where the propeller sits, plays a sweep
and tones, motor off. Acoustic reasoning and the alternatives are in
[`../../docs/acoustic-speculations/hub-source-options.md`](../../docs/acoustic-speculations/hub-source-options.md); that document governs
where the two disagree.

`hub-sphere.scad` is the model. The STLs are **not committed** — they are large and one
command regenerates them:

```bash
openscad -D 'part="onepiece"' -o onepiece.stl hub-sphere.scad   # the build
openscad -D 'part="section"'  -o section.png  hub-sphere.scad   # inspection render
admesh -b onepiece-print.stl onepiece.stl                        # tidies 17 stray normals
```

**One piece.** The only opening is the driver cutout, and the part prints with that flat
face on the bed. No split, no glue line, nothing to seal but the driver gasket and the
cable hole. The older split-at-the-equator halves are still in the file
(`part="top"` / `"bottom"`) but the one-piece is the build.

Every number is a parameter at the top of the file. The ones that matter:

| parameter | default | note |
|---|---|---|
| `volume_l` | 1.0 | **net** air volume, after the driver-flat cap, the apex cone and cone displacement are taken off |
| `wall` | 5.0 | shell thickness |
| `driver_cutout_d` | 75.0 | datasheet |
| `driver_flat_d` | 98.0 | seating face; must clear the 93 mm frame diagonal |
| `driver_displacement_ml` | 20 | estimate — see below, it barely matters |
| `boss_d` / `boss_h` | 30 / 24 | apex cone the M6 insert screws into |
| `land_t` | 8.0 | baffle land behind the seating face — see below, it is not optional |
| `screw_depth` | 6.0 | blind pilot depth into that land |

With the defaults: internal dia **127.5 mm**, external **137.5 mm**, overall printed height
**116.8 mm**, net 1000 ml → **Fc 181 Hz, Qtc 0.71** with the FRS 8 M (fs 125, Qts 0.49, Vas 1.1 l).

## Driver data — from the datasheet, not from guesswork

Visaton FRS 8 M, Art. No. 2001, 8 Ω. Datasheet PDF (drawing dated 27.07.2018, sheet
(c) 2023) held privately at `papers/datasheets/Visaton_2023_datasheet_FRS-8-M-2001.pdf`.

| | |
|---|---|
| cut-out | **Ø75 mm** |
| frame | **78 mm square** with corner tabs, **93 mm across the diagonal** |
| bolt circle | **Ø83 mm**, slots 4.5 × 5.5 mm |
| overall depth | **47 mm**, flange 2.1 mm |
| rated power / sensitivity | 30 W / 88 dB (1 W, 1 m) |
| xmech | ±2.5 mm |
| fs / impedance | 125 Hz / 8 Ω |

The frame being square is the trap: an 8 cm driver suggests a ~80 mm round flange, and an
earlier version of this model had an 88 mm seating flat, which the 93 mm diagonal would not
have sat on. The flat is now 98 mm, clearing by 2.5 mm per side.

The driver reaches to 2.8 mm past the centre of the sphere, against a cavity floor at
−63.4 mm, so there is no clash. `driver_displacement_ml` is still an estimate; it hardly
matters, because 20 ml against 60 ml moves Fc by about 2 Hz.

## Every hole in the part

| hole | size | where | notes |
|---|---|---|---|
| driver bore | **Ø75** | on the axis, through the seating face | the only opening; the driver closes it |
| driver screws | **4 × Ø3.2**, 6 mm deep | Ø83 bolt circle | **blind** — a through pilot would be four leaks |
| cable | **Ø6** | side wall, 12 mm below the equator | sealed with silicone once wired |
| M6 insert | **Ø8**, 10 mm deep | apex, on the axis | blind, into the solid cone |

Four holes, and only two of them go through into the cavity: the driver bore, which the
driver seals against its gasket, and the cable hole, which silicone seals.

**The land is why the screw holes work at all.** The cavity is a sphere, so where the
seating plane cuts it the opening is **83.4 mm** — wider than the 75 mm bore. Without a
land the seating face would be a 7 mm rim, and the screws at the 83 mm bolt circle would
come down in open air. `driver_land()` fills the ring from the bore out to the wall over
`land_t`, which restores a full 11.5 mm face and gives the screws 8 mm of material.

## Printing

Orientation: **driver flat down on the bed**, which is what `orient_for_print` produces.

- **Use a brim.** The first layer is an 11.5 mm wide ring under a part 116 mm tall. That is
  the one genuine risk in the print.
- The wall leans out at **45.8° from vertical** at the bed and gets more vertical from there
  to the equator, then closes as a dome. Right on the usual 45° rule — fine on most printers,
  and a couple of degrees of extra flat (`driver_flat_d`) buys margin if yours struggles.
- The apex is a **cone**, not a cylinder: printed this way up it widens as it rises and
  supports itself. A cylindrical boss would hang its whole underside in mid-air over the
  cavity. No support material is needed anywhere.
- The 6 mm cable hole is in the side wall where the wall is vertical, so it prints as one
  short bridge.
- **Seal the inside.** Printed walls leak through the layer lines and a leaky sealed
  box is not a sealed box. 4+ perimeters, then brush the interior with epoxy or
  sealant. This is the step most likely to be skipped and most likely to matter.
- ~10 g of loose polyester inside. The first internal mode of a 126 mm cavity is near
  1.9 kHz and a sphere focuses internal reflections at its centre, so do not omit it.
- Cable hole 6 mm, sealed with silicone once wired.
- The apex carries a blind hole for an M6 heat-set insert, drilled into solid cone
  material so it can never breach the sealed volume.
- Driver screw holes are 3.2 mm pilots on the datasheet's 83 mm circle — open them to
  4.3 mm for M4 clearance, or 5.6 mm for M4 heat-set inserts, whichever you prefer.

## Orientation in use

The driver fires **+Z, i.e. up**, along the rig's vertical axis — the direction the
propeller blew. With the arc flat, all eleven microphones then sit at the same polar
angle from the source, so the enclosure's directivity is a gain common to every
microphone and the fit absorbs it into the run-gain term.
