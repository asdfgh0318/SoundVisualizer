import { create } from 'zustand';
import type { MicAssignment } from '../types/index.ts';
import { ELEVATION_ANGLES } from '../types/index.ts';

interface DeviceState {
  devices: MediaDeviceInfo[];
  assignments: MicAssignment[];
  permissionGranted: boolean;
  error: string | null;

  enumerateDevices: () => Promise<void>;
  assignDevice: (elevationDeg: number, deviceId: string, label: string) => void;
  unassignDevice: (elevationDeg: number) => void;
  autoAssign: () => void;
  reset: () => void;
}

const initialAssignments: MicAssignment[] = ELEVATION_ANGLES.map((deg) => ({
  elevationDeg: deg,
  deviceId: '',
  label: '',
}));

export const useDeviceStore = create<DeviceState>((set, get) => ({
  devices: [],
  assignments: [...initialAssignments.map((a) => ({ ...a }))],
  permissionGranted: false,
  error: null,

  enumerateDevices: async () => {
    try {
      // Request mic permission first so we get real device labels
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      // Stop the temp stream immediately
      stream.getTracks().forEach((t) => t.stop());

      const allDevices = await navigator.mediaDevices.enumerateDevices();
      const audioInputs = allDevices.filter((d) => d.kind === 'audioinput');

      set({ devices: audioInputs, permissionGranted: true, error: null });
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to enumerate devices';
      set({ error: message, permissionGranted: false });
    }
  },

  assignDevice: (elevationDeg, deviceId, label) => {
    set((state) => ({
      assignments: state.assignments.map((a) =>
        a.elevationDeg === elevationDeg ? { ...a, deviceId, label } : a,
      ),
    }));
  },

  unassignDevice: (elevationDeg) => {
    set((state) => ({
      assignments: state.assignments.map((a) =>
        a.elevationDeg === elevationDeg ? { ...a, deviceId: '', label: '' } : a,
      ),
    }));
  },

  autoAssign: () => {
    const { devices } = get();
    const umikDevices = devices.filter(
      (d) => d.label.toLowerCase().includes('umik') || d.label.toLowerCase().includes('minidsp'),
    );

    if (umikDevices.length === 0) return;

    set((state) => ({
      assignments: state.assignments.map((a, i) => {
        if (i < umikDevices.length) {
          return {
            ...a,
            deviceId: umikDevices[i].deviceId,
            label: umikDevices[i].label,
          };
        }
        return a;
      }),
    }));
  },

  reset: () => {
    set({
      assignments: [...initialAssignments.map((a) => ({ ...a }))],
      error: null,
    });
  },
}));
