import { API_BASE } from './base';
import type {
  AudioDeviceInfo,
  CalibrationSummary,
  CaptureHalfRunRequest,
  CaptureRunStatus,
  CutoffTriggers,
  FakeCaptureResult,
  FFTResponse,
  FFTSettings,
  Key,
  MeasurementMeta,
  MicPresetEntry,
  PerformanceSummary,
  PWMPoint,
  SetupPreset,
  TytoStatus,
} from './types';

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
    this.name = 'ApiError';
  }
}

async function parseError(res: Response): Promise<string> {
  try {
    const body = await res.json();
    if (body?.detail) {
      return typeof body.detail === 'string' ? body.detail : JSON.stringify(body.detail);
    }
  } catch {
    /* not JSON */
  }
  return res.statusText || `HTTP ${res.status}`;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, init);
  if (!res.ok) throw new ApiError(res.status, await parseError(res));
  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}

const json = (body: unknown): RequestInit => ({
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(body),
});

export const api = {
  health: () => request<{ status: string }>('/health'),

  listAudioDevices: () => request<AudioDeviceInfo[]>('/devices/audio'),

  listCalibrations: () => request<CalibrationSummary[]>('/calibrations'),
  uploadCalibration: async (file: File, serial?: string): Promise<CalibrationSummary> => {
    const fd = new FormData();
    fd.append('file', file);
    const url = `/calibrations${serial ? `?serial=${encodeURIComponent(serial)}` : ''}`;
    const res = await fetch(`${API_BASE}${url}`, { method: 'POST', body: fd });
    if (!res.ok) throw new ApiError(res.status, await parseError(res));
    return res.json() as Promise<CalibrationSummary>;
  },

  listKeys: () => request<Key[]>('/keys'),
  createKey: (key: Pick<Key, 'motor' | 'propeller' | 'shroud' | 'notes'>) =>
    request<Key>('/keys', json(key)),
  getKey: (slug: string) => request<Key>(`/keys/${encodeURIComponent(slug)}`),
  listMeasurements: (slug: string) =>
    request<MeasurementMeta[]>(`/keys/${encodeURIComponent(slug)}/measurements`),

  tytoStatus: () => request<TytoStatus>('/tyto/status'),
  setTytoPwm: (pwm_us: number) => request<void>('/tyto/pwm', json({ pwm_us })),
  setTytoCutoffs: (cutoffs: CutoffTriggers) => request<void>('/tyto/cutoffs', json(cutoffs)),
  resetTytoWatchdog: () => request<void>('/tyto/reset', { method: 'POST' }),

  startCaptureRun: (body: CaptureHalfRunRequest) =>
    request<CaptureRunStatus>('/capture/run', json(body)),
  abortCaptureRun: () => request<void>('/capture/run', { method: 'DELETE' }),
  captureRunStatus: () => request<CaptureRunStatus>('/capture/run'),
  runFakeCapture: (body: CaptureHalfRunRequest) =>
    request<FakeCaptureResult>('/dev/fake_capture', json(body)),

  listSetupPresets: () => request<SetupPreset[]>('/setup-presets'),
  createSetupPreset: (name: string, mics: MicPresetEntry[]) =>
    request<SetupPreset>('/setup-presets', json({ name, mics })),
  deleteSetupPreset: (id: string) =>
    request<void>(`/setup-presets/${encodeURIComponent(id)}`, { method: 'DELETE' }),

  listPWMPoints: (slug: string) =>
    request<PWMPoint[]>(`/keys/${encodeURIComponent(slug)}/pwm_points`),
  getFFT: (slug: string, measId: string, settings: FFTSettings) =>
    request<FFTResponse>(
      `/keys/${encodeURIComponent(slug)}/measurements/${encodeURIComponent(measId)}/fft` +
        `?window=${settings.window}&size=${settings.size}&overlap=${settings.overlap}`,
    ),
  getPerformanceSummary: (slug: string, measId: string) =>
    request<PerformanceSummary>(
      `/keys/${encodeURIComponent(slug)}/measurements/${encodeURIComponent(measId)}/performance_summary`,
    ),
};
