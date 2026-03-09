import type { AudioCapture, Measurement, SplResult } from '../types/index.ts';

/**
 * Compute RMS (root mean square) of a Float32Array.
 */
export function computeRms(samples: Float32Array): number {
  if (samples.length === 0) return 0;
  let sum = 0;
  for (let i = 0; i < samples.length; i++) {
    sum += samples[i] * samples[i];
  }
  return Math.sqrt(sum / samples.length);
}

/**
 * Compute broadband SPL in dB (relative scale, 0 dB = full scale).
 * Returns -Infinity for silence.
 */
export function computeSplDb(samples: Float32Array): number {
  const rms = computeRms(samples);
  if (rms === 0) return -Infinity;
  return 20 * Math.log10(rms);
}

/**
 * Compute SPL from a single AudioCapture.
 */
export function captureSplDb(capture: AudioCapture): number {
  return computeSplDb(capture.audioData);
}

/**
 * Compute SPL results for all captures across all measurements.
 */
export function computeAllSpl(measurements: Measurement[]): SplResult[] {
  const results: SplResult[] = [];
  for (const m of measurements) {
    for (const c of m.captures) {
      results.push({
        azimuthDeg: m.azimuthDeg,
        elevationDeg: c.elevationDeg,
        splDb: computeSplDb(c.audioData),
      });
    }
  }
  return results;
}
