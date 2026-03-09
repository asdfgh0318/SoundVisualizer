export interface MicAssignment {
  elevationDeg: number;
  deviceId: string;
  label: string;
}

export interface AudioCapture {
  elevationDeg: number;
  deviceId: string;
  audioData: Float32Array;
  sampleRate: number;
  durationSec: number;
}

export interface Measurement {
  id: string;
  azimuthDeg: number;
  timestamp: number;
  captures: AudioCapture[];
}

export interface Session {
  id: string;
  name: string;
  createdAt: number;
  micAssignments: MicAssignment[];
  measurements: Measurement[];
  captureDurationSec: number;
  sampleRate: number;
}

export type CaptureStatus =
  | 'idle'
  | 'requesting'
  | 'recording'
  | 'processing'
  | 'done'
  | 'error';

export interface SplResult {
  azimuthDeg: number;
  elevationDeg: number;
  splDb: number;
}

export const ELEVATION_ANGLES = [-90, -45, 0, 45, 90] as const;
export type ElevationAngle = (typeof ELEVATION_ANGLES)[number];

/** Configuration for trigger-based multi-mic synchronization. */
export interface TriggerConfig {
  /** Whether to enable trigger-based alignment. */
  enabled: boolean;
  /** dBFS threshold — capture alignment starts when any mic exceeds this. */
  thresholdDb: number;
  /** Number of samples to analyze per block for trigger detection. */
  blockSize: number;
  /** Samples to keep before the trigger point (pre-roll). */
  prerollSamples: number;
}

export const DEFAULT_TRIGGER_CONFIG: TriggerConfig = {
  enabled: true,
  thresholdDb: -40,
  blockSize: 128,
  prerollSamples: 480, // 10ms at 48kHz
};

/** Approximate CEA-2034 broadband directivity metrics. */
export interface DirectivityMetrics {
  /** On-axis SPL (elevation=0, azimuth=0). */
  onAxisDb: number;
  /** Listening Window: avg SPL within ±30° horizontal, nearest vertical. */
  listeningWindowDb: number;
  /** Sound Power: solid-angle-weighted average over all measurements. */
  soundPowerDb: number;
  /** Directivity Index: on-axis minus sound power (in dB). */
  directivityIndexDb: number;
  /** Early Reflections: weighted average of reflection groups. */
  earlyReflectionsDb: number;
  /** Number of measurements used in computation. */
  measurementCount: number;
}
