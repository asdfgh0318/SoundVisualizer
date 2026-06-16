// Mirrors of server Pydantic schemas. Keep in sync with server/api/schemas.py.

export interface Key {
  motor: string;
  propeller: string;
  shroud: string;
  notes: string;
  slug: string;
}

/** 'full' = single-pass: all mics record simultaneously. 'top' / 'bottom' kept
 *  for legacy two-pass data + any future two-pass capture client. */
export type MeasurementHalf = 'top' | 'bottom' | 'full';

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
  alsa_card_id: string | null;
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
  tare_thrust_n: number;
  tare_torque_nm: number;
  tare_current_a: number;
}

export interface TareResponse {
  tare_thrust_n: number;
  tare_torque_nm: number;
  tare_current_a: number;
}

// Frontend-only: per-mic config persisted in localStorage. Single-pass: each
// mic has ONE elevation in [-90, +90]. (Two-pass rigs still supported by the
// backend; the wizard would issue two CaptureRunRequests with half=top/bottom
// — not exposed in this UI yet.)
export interface MicConfig {
  id: string;
  serial: string;
  deviceIndex: number | null;
  elevationDeg: number | null;
  calibrationFileId: string | null;
}

// Server-stored mic preset entry — no USB device since it shifts per machine.
// `elevation_deg` is the canonical field; `top_elevation_deg` /
// `bottom_elevation_deg` are kept readable so legacy presets still round-trip.
export interface MicPresetEntry {
  serial: string;
  elevation_deg: number | null;
  top_elevation_deg?: number | null;
  bottom_elevation_deg?: number | null;
  calibration_file_id: string | null;
}

export interface SetupPreset {
  id: string;
  name: string;
  created_at: string;
  mics: MicPresetEntry[];
}

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

export interface CaptureRunRequest {
  key: KeyFields;
  /** Single-pass rigs send 'full'. Two-pass clients can send 'top'/'bottom'
   *  to label their measurements; the backend accepts all three. */
  half: MeasurementHalf;
  pwm_steps: PWMStep[];
  mics: CaptureMicSpecRun[];
  sample_rate: number;
  stabilize_window: number;
  stabilize_tolerance: number;
  stabilize_timeout_seconds: number;
  trigger: CaptureTriggerConfig;
  /** Optional duct-research-tree linkage: server pushes Results URL back to
   *  this node on successful capture and flips status to 'in-progress'. */
  research_tree_node_id?: string | null;
}

// Research-tree integration
export interface ResearchTreePhase {
  id: string;
  title: string;
  color: string;
}

export interface ResearchTreeNode {
  id: string;
  phaseId: string;
  title: string;
  description?: string;
  type: 'test' | 'build' | 'synthesis' | 'decision' | string;
  status: 'planned' | 'in-progress' | 'done' | 'blocked' | string;
  parents: string[];
  geometry: {
    airGapMm?: number | null;
    ductHeightMm?: number | null;
    rodCountTop?: number | null;
    rodCountBottom?: number | null;
    weightG?: number | null;
    propellerInches?: number | null;
    motorSpacingMm?: number | null;
  };
  soundVisualizerLink?: string;
  notes?: string;
}

export interface ResearchTreeNodesResponse {
  enabled: boolean;
  base_url: string;
  phases: ResearchTreePhase[];
  nodes: ResearchTreeNode[];
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

export interface UnderlyingCapture {
  t_start: string;
  half: MeasurementHalf;
  performance_id: string | null;
  acoustic: AcousticInPoint[];
  performance_summary: PerformanceSummary | null;
}

/** A "merged PWM point" — all captures at the same PWM µs that pass compatibility
 *  check group into one of these. Incompatible captures end up in separate merged
 *  points (each with its own composition). */
export interface MergedPWMPoint {
  id: string; // "<pwm_us>-<group_index>"
  pwm_us: number;
  composition: Record<string, number>; // e.g. { top: 1, bottom: 1 } or { top: 2 }
  underlying: UnderlyingCapture[];
  acoustic: AcousticInPoint[]; // combined from all underlying, sorted by elev desc
  avg_performance: PerformanceSummary | null;
}

/** Legacy alias kept for the parts of the frontend that still expect the old name. */
export type PWMPoint = MergedPWMPoint;

export interface PsychoacousticMetrics {
  loudness_sone: number;
  sharpness_acum: number;
  roughness_asper: number;
  fluctuation_vacil: number;
  annoyance: number;
  fluctuation_assumed_zero: boolean;
}

export interface CompatTolerance {
  abs: number;
  rel: number;
}

export interface CompatibilityTolerances {
  thrust_n: CompatTolerance;
  torque_nm: CompatTolerance;
  current_a: CompatTolerance;
  voltage_v: CompatTolerance;
  rpm_mean: CompatTolerance;
}

export const COMPAT_CHANNELS: { key: keyof CompatibilityTolerances; label: string; unit: string }[] = [
  { key: 'thrust_n', label: 'Thrust', unit: 'N' },
  { key: 'torque_nm', label: 'Torque', unit: 'N·m' },
  { key: 'current_a', label: 'Current', unit: 'A' },
  { key: 'voltage_v', label: 'Voltage', unit: 'V' },
  { key: 'rpm_mean', label: 'RPM', unit: '' },
];

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
