import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type {
  CutoffChannel,
  CutoffChannelName,
  CutoffTriggers,
  MicConfig,
} from '../api/types';

const defaultCutoffs = (): CutoffTriggers => ({
  current: { enabled: false, threshold: 30,    direction: 'above' },
  voltage: { enabled: false, threshold: 14,    direction: 'below' },
  rpm:     { enabled: false, threshold: 25000, direction: 'above' },
  thrust:  { enabled: false, threshold: 100,   direction: 'above' },
  torque:  { enabled: false, threshold: 5,     direction: 'above' },
  temp0:   { enabled: false, threshold: 80,    direction: 'above' },
  temp1:   { enabled: false, threshold: 80,    direction: 'above' },
  temp2:   { enabled: false, threshold: 80,    direction: 'above' },
});

const newMic = (): MicConfig => ({
  id: crypto.randomUUID(),
  serial: '',
  deviceIndex: null,
  topElevationDeg: null,
  bottomElevationDeg: null,
  calibrationFileId: null,
});

interface SetupState {
  mics: MicConfig[];
  cutoffs: CutoffTriggers;
  // Bumped by CalibrationLibrary after upload — components watching this refetch.
  calibrationsVersion: number;
  addMic: () => void;
  updateMic: (id: string, patch: Partial<MicConfig>) => void;
  removeMic: (id: string) => void;
  replaceMics: (mics: MicConfig[]) => void;
  setCutoff: (channel: CutoffChannelName, patch: Partial<CutoffChannel>) => void;
  resetCutoffs: () => void;
  bumpCalibrations: () => void;
}

export const useSetupStore = create<SetupState>()(
  persist(
    (set) => ({
      mics: [],
      cutoffs: defaultCutoffs(),
      calibrationsVersion: 0,
      addMic: () => set((s) => ({ mics: [...s.mics, newMic()] })),
      updateMic: (id, patch) =>
        set((s) => ({
          mics: s.mics.map((m) => (m.id === id ? { ...m, ...patch } : m)),
        })),
      removeMic: (id) => set((s) => ({ mics: s.mics.filter((m) => m.id !== id) })),
      replaceMics: (mics) => set({ mics }),
      setCutoff: (channel, patch) =>
        set((s) => ({
          cutoffs: { ...s.cutoffs, [channel]: { ...s.cutoffs[channel], ...patch } },
        })),
      resetCutoffs: () => set({ cutoffs: defaultCutoffs() }),
      bumpCalibrations: () => set((s) => ({ calibrationsVersion: s.calibrationsVersion + 1 })),
    }),
    {
      name: 'soundvis-setup',
      partialize: (s) => ({ mics: s.mics, cutoffs: s.cutoffs }),
    },
  ),
);
