import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type {
  CutoffChannel,
  CutoffChannelName,
  CutoffTriggers,
  MicConfig,
} from '../api/types';
import { localId } from '../lib/uuid';

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
  id: localId(),
  serial: '',
  deviceIndex: null,
  elevationDeg: null,
  calibrationFileId: null,
});

/** Migrate persisted-localStorage entries that still carry the legacy
 *  `topElevationDeg` / `bottomElevationDeg` fields onto the new `elevationDeg`.
 *  Preserves the user's saved configuration across the schema change. */
function migrateMic(m: unknown): MicConfig {
  const x = m as Record<string, unknown>;
  const elev =
    typeof x.elevationDeg === 'number'
      ? x.elevationDeg
      : typeof x.topElevationDeg === 'number'
        ? x.topElevationDeg
        : typeof x.bottomElevationDeg === 'number'
          ? x.bottomElevationDeg
          : null;
  return {
    id: typeof x.id === 'string' ? x.id : localId(),
    serial: typeof x.serial === 'string' ? x.serial : '',
    deviceIndex: typeof x.deviceIndex === 'number' ? x.deviceIndex : null,
    elevationDeg: elev,
    calibrationFileId: typeof x.calibrationFileId === 'string' ? x.calibrationFileId : null,
  };
}

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
      version: 2,
      migrate: (persistedState) => {
        const s = (persistedState ?? {}) as { mics?: unknown[]; cutoffs?: CutoffTriggers };
        return {
          mics: Array.isArray(s.mics) ? s.mics.map(migrateMic) : [],
          cutoffs: s.cutoffs ?? defaultCutoffs(),
        };
      },
    },
  ),
);
