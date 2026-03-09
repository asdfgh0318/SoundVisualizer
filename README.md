# SoundVisualizer

Web-based polar sound distribution measurement tool. Captures raw audio from 5 UMIK-2 microphones arranged in a vertical arc and plots directivity patterns of sound sources on a turntable.

## Measurement Setup

```
        +90° (top)
         |
    +45° |
         |
  0° ----●---- object on turntable
         |
   -45°  |
         |
       -90° (bottom)
```

- 5 UMIK-2 USB mics at elevations: -90°, -45°, 0°, +45°, +90°
- Manual turntable rotation — user enters azimuth angle per capture
- Captures raw audio (WAV) from all 5 mics simultaneously
- Builds a spherical polar dataset across multiple azimuth positions
- Computes approximate CEA-2034 directivity metrics

## Tech Stack

React 19 + TypeScript + Vite 7 + Tailwind CSS 4 + Zustand. Zero external audio or chart dependencies — uses Web Audio API (AudioWorklet) for raw capture and custom SVG for visualization.

## Quick Start

```bash
npm install
npm run dev      # http://localhost:5173
npm run test     # vitest
npm run build    # production build
```

## Features

### Trigger-Based Multi-Mic Synchronization

Each UMIK-2 is an independent USB audio device with its own ADC clock. When captured via separate `getUserMedia()` calls, buffers may be offset by hundreds of samples due to USB scheduling jitter and driver latency differences.

**Solution:** After recording, each mic's buffer is scanned for the first block whose RMS exceeds a configurable dBFS threshold. All buffers are then trimmed to align on their respective trigger points, with a configurable pre-roll to preserve attack transients.

- **Threshold**: default -40 dBFS (adjustable -96 to 0)
- **Pre-roll**: default 10ms (preserves transient onset)
- **Block size**: 128 samples per RMS analysis block

This approach was informed by:
- **Klippel AN 54** — describes synchronization requirements for directivity measurement with turntable + vertical mic arc (our exact topology)
- **Klippel AN 69** — covers multi-mic array synchronization, spatial sampling, and interpolation for far-field directivity measurement

Implementation: [`src/audio/triggerSync.ts`](src/audio/triggerSync.ts)

### Approximate CEA-2034 Directivity Metrics

The Results page displays approximate broadband spinorama metrics computed from the sparse 5-elevation measurement grid:

| Metric | Description |
|--------|-------------|
| **On-Axis** | SPL at elevation=0°, azimuth=0° |
| **Listening Window** | Energy average within ±30° horizontal, elevation=0° |
| **Early Reflections** | Weighted average of floor, ceiling, front/side/rear wall reflection groups |
| **Sound Power** | Solid-angle-weighted energy average over all measurement positions |
| **Directivity Index** | On-axis minus Sound Power (in dB) |

**Solid-angle weighting**: Each elevation band's contribution is weighted by `sin(upper) - sin(lower)` of its boundary angles, correctly accounting for the fact that equatorial measurements cover more spherical surface area than polar ones.

**Limitations**: Full CEA-2034 requires 70 measurement positions (10° increments) with frequency-dependent SPL. Our 5-elevation broadband approximation gives useful directional metrics but should not be compared directly to full spinorama data.

This was built following methodology from:
- **Audiomatica AN-022** — step-by-step derivation of spinorama curves from polar measurement sets
- **pierreaubert/spinorama** — open-source CEA-2034 computation algorithms (Python)
- **Speaker Data 2034 Blog** — CEA-2034 angle group definitions

Implementation: [`src/audio/spinorama.ts`](src/audio/spinorama.ts)

### Audio Capture Engine

- Parallel `getUserMedia()` for 5 mics with AudioWorklet ring-buffer recording
- Single `AudioContext` at 48kHz, all processing disabled (no AGC, noise suppression, or echo cancellation)
- WAV export in 16-bit PCM or 32-bit float

### Custom SVG Polar Plot

- Elevation mapped to radius (center = +90° top, edge = -90° bottom)
- Azimuth mapped to angle (0° up, clockwise)
- Blue-yellow-red color scale for SPL intensity
- Hover tooltips with exact values

## Architecture

```
5x UMIK-2 → getUserMedia → AudioWorklet → Float32Array → Trigger Sync → Zustand store
                                                   ↓                           ↓
                                             WAV download              SPL computation
                                                                            ↓
                                                              ┌─── Polar Plot (SVG)
                                                              └─── Directivity Metrics (CEA-2034 approx)
```

## Pages

1. **Setup** — enumerate audio devices, assign each to an elevation slot
2. **Capture** — enter azimuth, set duration, configure trigger sync, capture
3. **Results** — interactive polar plot, directivity metrics, WAV export

## Reference Documents

The following research papers informed the measurement methodology and are saved in [`docs/references/`](docs/references/):

| Document | Applied To |
|----------|-----------|
| [Klippel AN 54: Directivity Measurement with Turntables](docs/references/Klippel_AN54_Directivity_Turntables.pdf) | Overall measurement topology (turntable + vertical mic arc), synchronization requirements, angular sampling strategy |
| [Klippel AN 69: Far Field Measurement using Mic Arrays](docs/references/Klippel_AN69_Far_Field_Mic_Arrays.pdf) | Multi-mic array design, trigger-based synchronization approach, spatial interpolation principles |
| [ARTA AN6: Directivity Measurements](docs/references/ARTA_AN6_Directivity_Measurements.pdf) | Measurement procedure, data processing pipeline, polar plot presentation conventions |
| [Audiomatica AN-022: Spinorama from Polar Data](docs/references/Audiomatica_AN022_Spinorama_From_Polar.pdf) | CEA-2034 computation: angle group definitions, solid-angle weighting, energy averaging for Listening Window / Early Reflections / Sound Power |

### How Each Reference Was Applied

**Klippel AN 54 + AN 69** → Trigger sync (`triggerSync.ts`). These papers describe measuring loudspeaker directivity with turntable + mic arc — exactly our setup. AN 69 specifically discusses the clock synchronization problem between independent microphones and recommends onset-based alignment, which we implement as dBFS threshold trigger detection with configurable pre-roll.

**ARTA AN6** → Polar plot conventions (`PolarPlot.tsx`). The elevation-to-radius mapping, azimuth spoke layout, and SPL color scaling follow conventions established in ARTA's directivity visualization.

**Audiomatica AN-022** → Spinorama computation (`spinorama.ts`). The solid-angle weighting formula, angle group definitions for Listening Window (±30°H, ±10°V), Early Reflections (floor/ceiling/wall groups), and Sound Power (full sphere average) come directly from this application note's derivation of CEA-2034 from polar measurement data.
