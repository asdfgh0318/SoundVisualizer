# Hub sound source for the loudspeaker session

Written 2026-09-09. Needed for campaign session 2 (report `arc-validation-remedies.pdf` §15):
a source that sits where the propeller sits, plays a 20 Hz–20 kHz exponential sweep and
tones at 216/238/258 Hz, recorded by all 11 microphones with the motor off.

## Requirements, derived from our own captures

| requirement | value | why |
|---|---|---|
| level | ~60 dB SPL at 0.84 m is enough | the propeller itself gave 25–62 dB per third-octave, 67 dB overall; a 10 s sweep adds ~50 dB of processing gain |
| size | 10–20 cm | it replaces a 15 cm propeller; anything larger becomes the reflector we are trying to find |
| omnidirectional | to at least 1 kHz | the reflector question lives at 200–1000 Hz. ka=1 limit: 6 cm piston → 1.8 kHz, 11 cm → 1.0 kHz |
| enclosure | sealed, single driver | must be quiet before the echoes at 2.0 ms (−72°) and 4.4 ms (+36°/+54°); a crossover would make two sources |
| bandwidth | ≥8 kHz usable | resolves 0.125 ms; the shortest echo of interest is 0.58 ms |

Timing, not amplitude flatness, is what the analysis needs, so beaming above 2 kHz is tolerable.

## Options, all verified on the vendor's own page 2026-09-09

**Borrow first.** PW Zakład Elektroakustyki (IRiTM) lists "laboratoryjne źródła dźwięku"
among its Brüel & Kjær equipment, plus a 300 m³ anechoic chamber and Dirac, and offers
measurements to outside parties: <https://zea.ire.pw.edu.pl/oferta/>. Models are not
published. Contact: prof. Jan Żera (Jan.Zera@ire.pw.edu.pl, +48 22 234 7999),
dr Marcin Lewandowski (+48 22 234 7637), dr G. Makarewicz (+48 22 234 7748).
Ask specifically for the **B&K OmniSource 4295**: single driver through a conical coupler
to a small orifice, 50–6300 Hz, Ø145 × 560 mm, 3.5 kg, Lw 105 dB broadband and ≥85 dB per
third-octave (datasheet bp2103). Its long thin body sits down the stand axis, so it is the
only professional source that fits the hub. PL distributor JPT VIBRO (Warszawa), quote only.

**Buy ready-made.** Avantone Active MixCube, single, 1222 zł at thomann.pl. Sealed 18 mm MDF
with Dacron stuffing, one 5.25" paper cone, no tweeter and no crossover, 200 Hz–10 kHz
(no tolerance stated), 104 dB at 1 m, XLR/TRS input, 165 mm cube, 60 W built in.
The only sealed single-driver active found. Genelec 8010A, Neumann KH 80, Yamaha HS3 and
IK iLoud are all bass-reflex; Adam D3V uses passive radiators.

**Build.** Visaton FRS 8 M 8 Ω, 58 zł at thomann.pl (73.70 zł at grelton.pl, the Polish
Visaton distributor). Sd 29 cm² = 6.1 cm effective piston, so omnidirectional to ~1.8 kHz;
fs 125 Hz, Qts 0.49, Vas 1.1 l, 88 dB/1 W/1 m. In a **1.0 litre sealed box** (a 10 cm cube,
lightly stuffed) the alignment is Butterworth: Fc 181 Hz, Qtc 0.71.

| band | 125 | 157 | 198 | 250 | 315 | 400 Hz |
|---|---|---|---|---|---|---|
| output re passband | −7.3 | −4.4 | −2.3 | −1.0 | −0.4 | −0.2 dB |

At 88 dB/W it makes ~95 dB at 1 m on a few watts against the ~60 dB needed, so even the
125 Hz band has 25 dB of margin. Amplifier: TPA3116 board with a 3.5 mm input, 180 zł at
gotronik.pl, or SMSL A100 (40 W into 8 Ω, RCA line in), 449 zł at mp3store.pl.

**Not suitable.** Measurement dodecahedrons are 25–39 cm and 4.5–8 kg (Svantek SV 90/103
250 mm, Norsonic Nor283 270 mm, B&K OmniPower 4292-L 390 mm). At the hub they would replace
the propeller with a large obstacle. No Polish vendor publishes a price for any measurement
source; all are quote-only.

## Still missing on our side

No sweep tooling exists: no playback path in the server, no sweep generator, no
deconvolution script. Needed before the session, not after.
