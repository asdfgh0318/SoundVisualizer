// Mirrors of server Pydantic schemas. Keep in sync with server/api/schemas.py.

export interface Key {
  motor: string;
  propeller: string;
  shroud: string;
  notes: string;
  slug: string;
}

export type MeasurementHalf = 'top' | 'bottom';

export interface AcousticMeasurementMeta {
  type: 'acoustic';
  id: string;
  t_start: string;
  t_end: string;
  pwm_setpoint: number | null;
  mic_serial: string;
  elevation_deg: number;
  azimuth_deg: number | null;
  half: MeasurementHalf;
  sample_rate: number;
  calibration_file_id: string | null;
}

export interface PerformanceMeasurementMeta {
  type: 'performance';
  id: string;
  t_start: string;
  t_end: string;
  pwm_setpoint: number | null;
}

export interface NorsonicMeasurementMeta {
  type: 'norsonic';
  id: string;
  t_start: string;
  t_end: string;
  pwm_setpoint: number | null;
}

export type MeasurementMeta =
  | AcousticMeasurementMeta
  | PerformanceMeasurementMeta
  | NorsonicMeasurementMeta;

export interface AudioDeviceInfo {
  index: number;
  name: string;
  hostapi: string;
  max_input_channels: number;
  default_samplerate: number;
}

export interface CalibrationSummary {
  id: string;
  serial: string | null;
  sens_factor_db: number | null;
  again_db: number | null;
  n_points: number;
  freq_min_hz: number;
  freq_max_hz: number;
}

export type CutoffDirection = 'above' | 'below';

export interface CutoffChannel {
  enabled: boolean;
  threshold: number;
  direction: CutoffDirection;
}

export type CutoffChannelName =
  | 'current' | 'voltage' | 'rpm'
  | 'thrust' | 'torque'
  | 'temp0' | 'temp1' | 'temp2';

export type CutoffTriggers = Record<CutoffChannelName, CutoffChannel>;

export interface TytoStatus {
  connected: boolean;
  pwm_us: number | null;
  tripped: string | null;
}

// Frontend-only: per-mic config persisted in localStorage.
export interface MicConfig {
  id: string;
  serial: string;
  deviceIndex: number | null;
  topElevationDeg: number | null;
  bottomElevationDeg: number | null;
  calibrationFileId: string | null;
}

export const ELEVATION_VALUES = [
  -90, -75, -60, -45, -30, -15, 0, 15, 30, 45, 60, 75, 90,
] as const;

// Capture wizard

export interface PWMStep {
  pwm_us: number;
  recording_ms: number;
}

export interface KeyFields {
  motor: string;
  propeller: string;
  shroud: string;
  notes: string;
}

export type CaptureRunPhase =
  | 'idle'
  | 'starting'
  | 'setting_pwm'
  | 'stabilizing'
  | 'recording'
  | 'writing'
  | 'spooling_down'
  | 'completed'
  | 'failed'
  | 'aborted';

export type CaptureRunState = 'idle' | 'running' | 'completed' | 'failed' | 'aborted';

export interface CaptureRunStatus {
  run_id: string;
  state: CaptureRunState;
  phase: CaptureRunPhase;
  half: MeasurementHalf | null;
  key_slug: string | null;
  current_step: number;
  total_steps: number;
  current_pwm_us: number | null;
  measurement_ids: string[];
  error: string | null;
}

export interface CaptureMicSpecRun {
  serial: string;
  device_index: number;
  elevation_deg: number;
  calibration_file_id: string | null;
}

export interface CaptureTriggerConfig {
  enabled: boolean;
  threshold_db: number;
  block_size: number;
  preroll_samples: number;
}

export interface CaptureHalfRunRequest {
  key: KeyFields;
  half: MeasurementHalf;
  pwm_steps: PWMStep[];
  mics: CaptureMicSpecRun[];
  sample_rate: number;
  stabilize_window: number;
  stabilize_tolerance: number;
  stabilize_timeout_seconds: number;
  trigger: CaptureTriggerConfig;
}

export interface FakeCaptureResult {
  key: string;
  measurement_ids: string[];
}

export interface TelemetryFrame {
  t: string;
  pwm_us: number;
  thrust_n: number;
  torque_nm: number;
  current_a: number;
  voltage_v: number;
  rpm: number;
  temp0_c: number;
  temp1_c: number;
  temp2_c: number;
  vibration: number;
  tripped: string | null;
}

// Results

export interface AcousticInPoint {
  id: string;
  mic_serial: string;
  elevation_deg: number;
  half: MeasurementHalf;
  calibration_file_id: string | null;
}

export interface PWMPoint {
  t_start: string;
  half: MeasurementHalf | null;
  pwm_us: number | null;
  performance_id: string | null;
  acoustic: AcousticInPoint[];
}

export interface FFTResponse {
  frequencies: number[];
  magnitudes_db: number[];
  sample_rate: number;
  calibrated: boolean;
  window: string;
  size: number;
}

export interface PerformanceSummary {
  n_samples: number;
  duration_s: number;
  thrust_n_mean: number;
  thrust_n_max: number;
  torque_nm_mean: number;
  current_a_mean: number;
  voltage_v_mean: number;
  rpm_mean: number;
  temp0_c_max: number;
  temp1_c_max: number;
  temp2_c_max: number;
}

export interface FFTSettings {
  window: 'hann';
  size: number;
  overlap: number;
}

export const FFT_SIZE_OPTIONS = [1024, 2048, 4096, 8192, 16384] as const;
export const FFT_OVERLAP_OPTIONS = [0, 0.25, 0.5, 0.75] as const;
