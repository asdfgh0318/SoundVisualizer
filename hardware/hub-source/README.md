# Hub loudspeaker enclosure — 1 litre sealed sphere

For campaign session 2: a source that sits where the propeller sits, plays a sweep
and tones, motor off. Acoustic reasoning and the alternatives are in
[`../../docs/hub-source-options.md`](../../docs/hub-source-options.md); that document governs
where the two disagree.

`hub-sphere.scad` is the model. The STLs are **not committed** — they are 16 MB and one
command regenerates them:

```bash
openscad -D 'part="bottom"' -o bottom.stl hub-sphere.scad
openscad -D 'part="top"'    -o top.stl    hub-sphere.scad
openscad -D 'part="section"' -o section.png hub-sphere.scad   # inspection render
```

Every number is a parameter at the top of the file. The ones that matter:

| parameter | default | note |
|---|---|---|
| `volume_l` | 1.0 | **net** air volume, after the driver-flat cap and cone displacement are added back |
| `wall` | 5.0 | shell thickness |
| `driver_cutout_d` | 75.0 | FRS 8 M datasheet |
| `driver_flat_d` | 88.0 | seating face — **verify against the frame in your hand** |
| `driver_displacement_ml` | 20 | estimate; measure the driver and correct it |
| `fit_clr` | 0.25 | spigot clearance, loosen on a sloppy printer |

With the defaults: internal dia **125.8 mm**, external **135.8 mm**, net 1000 ml,
so Fc 181 Hz / Qtc 0.71 with the FRS 8 M (fs 125, Qts 0.49, Vas 1.1 l).

## Printing

- Two hemispheres, split at the equator, located by a spigot that sits in the inner
  half of the wall so the outside stays flush. Glue and seal on assembly.
- **Seal the inside.** Printed walls leak through the layer lines and a leaky sealed
  box is not a sealed box. 4+ perimeters, then brush the interior with epoxy or
  sealant. This is the step most likely to be skipped and most likely to matter.
- ~10 g of loose polyester inside. The first internal mode of a 126 mm cavity is near
  1.9 kHz and a sphere focuses internal reflections at its centre, so do not omit it.
- Cable hole is 6 mm, off-axis by 25 mm, sealed with silicone.
- The south pole carries a flat pad with a blind hole for an M6 heat-set insert, with
  solid material behind it so the insert never breaks into the sealed volume.
- Screw holes for the driver are **off** by default — drill them after measuring the
  real frame rather than trusting a guessed bolt circle.

## Orientation in use

The driver fires **+Z, i.e. up**, along the rig's vertical axis — the direction the
propeller blew. With the arc flat, all eleven microphones then sit at the same polar
angle from the source, so the enclosure's directivity is a gain common to every
microphone and the fit absorbs it into the run-gain term.
