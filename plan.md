# SoundVisualizer - Polar Sound Distribution Measurement Tool

## Goal

Web tool for capturing raw audio from 5 UMIK-2 microphones arranged in a vertical arc and plotting polar sound distribution. Standalone, but designed to be embeddable into existing web sound acquisition software.

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
- Builds up spherical polar dataset across multiple azimuth positions

## Tech Stack

- React 19 + TypeScript + Vite 7 + Tailwind CSS 4
- Zustand for state management
- Web Audio API (AudioWorklet) for raw audio capture
- Custom SVG polar plot (no chart library)
- Zero extra runtime dependencies

## Architecture

### Core Modules
- **captureEngine.ts** — parallel getUserMedia + AudioWorklet for 5 simultaneous mic capture
- **recorderProcessor.ts** — AudioWorklet processor (audio thread ring-buffer recorder)
- **wavEncoder.ts** — Float32Array → WAV blob (16-bit or 32-bit PCM)
- **spl.ts** — RMS-based SPL computation from raw audio
- **spinorama.ts** — approximate CEA-2034 directivity metrics
- **triggerSync.ts** — trigger-based multi-mic synchronization
- **PolarPlot.tsx** — custom SVG polar distribution visualization

### Data Flow
```
5x UMIK-2 → getUserMedia → AudioWorklet → Float32Array → Zustand store
                                                ↓               ↓
                                          WAV download    SPL computation → Polar Plot
```

### Pages
1. **Setup** — enumerate audio devices, assign each to an elevation slot
2. **Capture** — enter azimuth, set duration, click capture, see measurement list
3. **Results** — interactive polar plot + WAV export + directivity metrics

## Implementation Phases

1. **Scaffolding + Device Setup** — project init, device enumeration, mic assignment UI
2. **Audio Capture Engine** — AudioWorklet recorder, multi-mic capture, capture UI
3. **WAV Export + Data Management** — WAV encoding, measurement list, bulk download
4. **Polar Visualization** — SPL computation, SVG polar plot, results page
5. **Polish** — guided sequence mode, frequency-selective SPL, session save/load

## Key Decisions

- AudioWorklet over MediaRecorder (raw PCM access, no lossy encoding)
- Single AudioContext at 48kHz (shared for all 5 streams)
- In-memory storage (no IndexedDB), explicit WAV download
- Chrome-first (best AudioWorklet support)
- Custom SVG polar plot (simple, zero-dep, full control)
- Trigger-based sync for multi-mic alignment
