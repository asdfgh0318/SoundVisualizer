# Averaging over source rotations — what the literature says

**Status: literature only. We have not done this.** Written 2026-09-23 after the
2026-09-17 session found our own sphere is not axisymmetric at 3–5 kHz.

## Why this is here

On 2026-09-17 we measured that the printed 1 l sphere holds axisymmetry to 3 kHz and
fails in a narrow band around 4.4 kHz — an m = 1 rocking mode of the cone, 11.0 dB at
4362 Hz, found by remounting the driver 180° inside an enclosure that never moved. The
obvious remedy is to capture at several source roll angles and average, so the
angular-order components cancel. That remedy was my suggestion, not a measurement, and it
turns out to be established practice.

## The two quotes

Papadakis, N. M. & Stavroulakis, G. E., *Low Cost Omnidirectional Sound Source Utilizing a
Common Directional Loudspeaker for Impulse Response Measurements*, Applied Sciences 8(9),
2018. Held at `papers/SoundVisualizer/arc-validation/Papadakis_2018_ApplSci_directional-speaker-as-omni-source.pdf`.

> "Different placements of the loudspeakers were performed (twelve positions similar to the
> twelve positions of the faces of a dodecahedron speaker, different rotations of the
> loudspeakers for a total sum of twenty six and fourteen positions). The impulse responses
> obtained were added up creating a single impulse response for each case."
> — abstract, **p. 1**

> "The directivity of a dodecahedron speaker can be considered uniform in the low-frequency
> range (namely below 1 kHz), while at higher frequencies sound radiation shows greater
> deviation [7]. Stepwise rotation of dodecahedron speaker can be employed to improve the
> accuracy of room acoustic measurements [8]."
> — introduction, **p. 2**

## What that does and does not tell us

**It supports the remedy.** Summing responses taken at several orientations of an ordinary
directional loudspeaker is a published method for synthesising an omnidirectional source,
and stepwise rotation is already used to improve even a dodecahedron.

**It reframes our result.** A dodecahedron — the standard instrument, far more expensive
than our sphere — is described as uniform only **below 1 kHz**. Ours holds to **3 kHz** on
our own measurement. By that comparison the sphere is not a poor source; it is a good one
with a known narrow defect.

**It does not transfer directly.** Papadakis measures room impulse responses and reverberation
parameters, and the acceptance is a mean absolute error in reverberation time. We are
measuring a **per-position level map** across eleven fixed capsules at single tones, which is
a different quantity with a different error budget. Nothing in the paper says what rotation
averaging does to *our* measurement, and the paper's own numbers are about its three rooms,
not ours.

**What would move this out of this folder:** capture the same tone grid at 0°, 90°, 180° and
270° of source roll, average, and show that the 3–5 kHz band comes back to the ~0.2 dB the
rest of the range already reaches. Two runs of that pair already exist (`roll-B` at 0° and
`driver-180` at 180°); it needs the two quarter-turns and the arithmetic.
