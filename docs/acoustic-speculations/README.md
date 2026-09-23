# Acoustic speculations

Nothing in this folder is tied to a measurement of **our** chamber. It is literature,
other people's facilities, priced options, and reasoning about what our rig probably does.
Useful for deciding what to try next; not evidence about our room.

The split is deliberate. Everything one level up — `arc-rig-onepager.pdf`, `mic_arc.md`,
`analysis/` — is grounded in captures we took and can re-run. Everything here is not, and
the two kinds should never be quoted in the same breath.

| file | what it is | how far it is from our chamber |
|---|---|---|
| `chamber-fighting-guide.pdf` (+ `.html`) | 11 pp. methods menu built from 69 held papers and 29 named facilities in 17 countries: per method the lowest usable frequency, residual error, cost and failure mode. All 94 quotes verified verbatim against the text dumps. | **Other people's rooms.** Every number is theirs. Nothing in it has been tested here. The nearest thing to applicable is du Plessis 2022's measured per-position room correction (<0.55 dB above 200 Hz for a non-conforming fan facility), and whether that transfers to us is untested. |
| `reflection-localization.html` | How to locate a reflection once a room fails qualification — method from Sun 2012 / Mabande 2013, re-verified 5/5 on 2026-09-09. | **Method we have not run.** We do have a real target for it: extra path 1.5 m at +36°/+54° and 0.7 m at −72°, the 630–1000 Hz band. Until we run it, this is a plan. |
| `hub-source-options.md` | Source options and prices: B&K OmniSource 4295 on loan from PW Zakład Elektroakustyki, Avantone MixCube, the Visaton FRS 8 M sphere, why dodecahedrons are too big for the hub. | **Mostly untested.** We built the FRS 8 M sphere from it and then measured that it is only axisymmetric below 3 kHz (an m = 1 rocking mode, 11.0 dB at 4362 Hz). The claims about the sources we did *not* buy remain unchecked. The OmniSource loan is the one live action item in here. |
| `recirculation-plan.html` | Why an ascending-PWM sequence lets a wake build over a whole run, and what to change in the sequence. | **Reasoning, not measurement.** Plausible and worth acting on, but we have never measured recirculation in this room. |

## What would move a file out of here

A capture in `calibrator/sessions/` or the measurement repo that tests the claim in our room,
with the numbers written into the one-pager. Until then it stays a speculation, however good
the source.
