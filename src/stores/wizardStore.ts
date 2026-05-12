import { create } from 'zustand';
import type { CaptureRunStatus } from '../api/types';

export type WizardPhase =
  | 'form'
  | 'review'
  | 'safety'
  | 'running_top'
  | 'reconfigure'
  | 'running_bottom'
  | 'done'
  | 'failed';

export interface WizardForm {
  motor: string;
  propeller: string;
  shroud: string;
  notes: string;
  sample_rate: number;
  pwm_steps: { pwm_us: number; recording_ms: number }[];
  stabilize_window: number;
  stabilize_tolerance: number;
  stabilize_timeout_seconds: number;
  run_top: boolean;
  run_bottom: boolean;
  selected_mic_ids: string[];
  trigger: {
    enabled: boolean;
    threshold_db: number;
    block_size: number;
    preroll_samples: number;
  };
}

const defaultForm = (): WizardForm => ({
  motor: '',
  propeller: '',
  shroud: '',
  notes: '',
  sample_rate: 48000,
  pwm_steps: [
    { pwm_us: 1200, recording_ms: 1000 },
    { pwm_us: 1500, recording_ms: 1500 },
    { pwm_us: 1800, recording_ms: 2000 },
  ],
  stabilize_window: 10,
  stabilize_tolerance: 4.0,
  stabilize_timeout_seconds: 30.0,
  run_top: true,
  run_bottom: true,
  selected_mic_ids: [],
  trigger: { enabled: true, threshold_db: -40, block_size: 128, preroll_samples: 480 },
});

interface WizardState {
  phase: WizardPhase;
  form: WizardForm;
  status: CaptureRunStatus | null;
  activeRunId: string | null;
  topMeasurementIds: string[];
  bottomMeasurementIds: string[];
  errorMessage: string | null;
  setPhase: (p: WizardPhase) => void;
  updateForm: (patch: Partial<WizardForm>) => void;
  setForm: (form: WizardForm) => void;
  resetForm: () => void;
  setStatus: (s: CaptureRunStatus | null) => void;
  setActiveRunId: (id: string | null) => void;
  setTopIds: (ids: string[]) => void;
  setBottomIds: (ids: string[]) => void;
  setError: (msg: string | null) => void;
  reset: () => void;
}

export const useWizardStore = create<WizardState>((set) => ({
  phase: 'form',
  form: defaultForm(),
  status: null,
  activeRunId: null,
  topMeasurementIds: [],
  bottomMeasurementIds: [],
  errorMessage: null,
  setPhase: (p) => set({ phase: p }),
  updateForm: (patch) => set((s) => ({ form: { ...s.form, ...patch } })),
  setForm: (form) => set({ form }),
  resetForm: () => set({ form: defaultForm() }),
  setStatus: (s) => set({ status: s }),
  setActiveRunId: (id) => set({ activeRunId: id }),
  setTopIds: (ids) => set({ topMeasurementIds: ids }),
  setBottomIds: (ids) => set({ bottomMeasurementIds: ids }),
  setError: (msg) => set({ errorMessage: msg }),
  reset: () =>
    set({
      phase: 'form',
      status: null,
      activeRunId: null,
      topMeasurementIds: [],
      bottomMeasurementIds: [],
      errorMessage: null,
    }),
}));
