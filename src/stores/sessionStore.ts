import { create } from 'zustand';
import type { Measurement, CaptureStatus, TriggerConfig } from '../types/index.ts';
import { DEFAULT_TRIGGER_CONFIG } from '../types/index.ts';

interface SessionState {
  sessionName: string;
  measurements: Measurement[];
  captureStatus: CaptureStatus;
  captureProgress: number;
  captureDurationSec: number;
  sampleRate: number;
  currentAzimuth: number;
  errorMessage: string | null;
  triggerConfig: TriggerConfig;

  setSessionName: (name: string) => void;
  setCurrentAzimuth: (deg: number) => void;
  setCaptureDuration: (sec: number) => void;
  setCaptureStatus: (status: CaptureStatus) => void;
  setCaptureProgress: (pct: number) => void;
  setError: (msg: string | null) => void;
  addMeasurement: (m: Measurement) => void;
  deleteMeasurement: (id: string) => void;
  suggestNextAzimuth: () => number;
  setTriggerConfig: (config: Partial<TriggerConfig>) => void;
  clearSession: () => void;
}

export const useSessionStore = create<SessionState>((set, get) => ({
  sessionName: '',
  measurements: [],
  captureStatus: 'idle',
  captureProgress: 0,
  captureDurationSec: 3,
  sampleRate: 48000,
  currentAzimuth: 0,
  errorMessage: null,
  triggerConfig: DEFAULT_TRIGGER_CONFIG,

  setSessionName: (name) => set({ sessionName: name }),
  setCurrentAzimuth: (deg) => set({ currentAzimuth: deg }),
  setCaptureDuration: (sec) => set({ captureDurationSec: sec }),
  setCaptureStatus: (status) => set({ captureStatus: status }),
  setCaptureProgress: (pct) => set({ captureProgress: pct }),
  setError: (msg) => set({ errorMessage: msg }),

  addMeasurement: (m) =>
    set((state) => ({
      measurements: [...state.measurements, m],
      captureStatus: 'done',
    })),

  deleteMeasurement: (id) =>
    set((state) => ({
      measurements: state.measurements.filter((m) => m.id !== id),
    })),

  suggestNextAzimuth: () => {
    const { measurements } = get();
    const taken = new Set(measurements.map((m) => m.azimuthDeg));
    // Suggest in 15-degree steps from 0 to 345
    for (let a = 0; a < 360; a += 15) {
      if (!taken.has(a)) return a;
    }
    return 0;
  },

  setTriggerConfig: (config) =>
    set((state) => ({
      triggerConfig: { ...state.triggerConfig, ...config },
    })),

  clearSession: () =>
    set({
      sessionName: '',
      measurements: [],
      captureStatus: 'idle',
      captureProgress: 0,
      currentAzimuth: 0,
      errorMessage: null,
    }),
}));
