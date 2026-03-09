import type { AudioCapture, TriggerConfig } from '../types/index.ts';

/**
 * Trigger-based multi-microphone synchronization.
 *
 * Problem: Each UMIK-2 is an independent USB audio device with its own ADC clock.
 * When captured via separate getUserMedia() calls, there is no sample-accurate
 * alignment — buffers may be offset by hundreds of samples due to USB scheduling
 * jitter and driver latency differences.
 *
 * Solution: Use the sound onset itself as a synchronization reference.
 * After capturing, scan each mic's buffer for the first sample block whose RMS
 * exceeds a dBFS threshold. Trim all buffers to align on their respective
 * trigger points, keeping a configurable pre-roll for attack transients.
 *
 * Based on principles from:
 * - Klippel AN 54: Directivity Measurement with Turntables
 * - Klippel AN 69: Far Field Measurement using Microphone Arrays
 * Both describe multi-mic array synchronization for directivity measurement.
 */

/**
 * Compute RMS of a block of samples in dBFS.
 */
function blockRmsDb(samples: Float32Array, offset: number, blockSize: number): number {
  const end = Math.min(offset + blockSize, samples.length);
  const count = end - offset;
  if (count <= 0) return -Infinity;

  let sum = 0;
  for (let i = offset; i < end; i++) {
    sum += samples[i] * samples[i];
  }
  const rms = Math.sqrt(sum / count);
  return rms === 0 ? -Infinity : 20 * Math.log10(rms);
}

/**
 * Find the sample index where the signal first exceeds the threshold.
 * Returns -1 if the signal never exceeds the threshold.
 */
export function findTriggerIndex(
  samples: Float32Array,
  thresholdDb: number,
  blockSize: number,
): number {
  for (let offset = 0; offset < samples.length; offset += blockSize) {
    if (blockRmsDb(samples, offset, blockSize) >= thresholdDb) {
      return offset;
    }
  }
  return -1;
}

/**
 * Align multiple audio captures using trigger-based synchronization.
 *
 * Each capture's buffer is scanned for the first block exceeding thresholdDb.
 * All buffers are then trimmed so their trigger points align, with prerollSamples
 * of audio preserved before the trigger for capturing attack transients.
 *
 * If a mic never triggers (e.g., silence), it is kept but trimmed to match
 * the shortest aligned buffer length.
 *
 * @returns New AudioCapture array with aligned audioData buffers.
 */
export function alignCaptures(
  captures: AudioCapture[],
  config: TriggerConfig,
): AudioCapture[] {
  if (!config.enabled || captures.length === 0) return captures;

  const triggerIndices = captures.map((c) =>
    findTriggerIndex(c.audioData, config.thresholdDb, config.blockSize),
  );

  // If no mic triggered, return captures as-is
  if (triggerIndices.every((idx) => idx === -1)) return captures;

  // Compute the trim start for each capture: trigger index minus preroll, clamped to 0
  const trimStarts = triggerIndices.map((idx) => {
    if (idx === -1) return 0; // didn't trigger — use beginning
    return Math.max(0, idx - config.prerollSamples);
  });

  // Find the minimum remaining length after trimming
  const remainingLengths = captures.map(
    (c, i) => c.audioData.length - trimStarts[i],
  );
  const minLength = Math.min(...remainingLengths);

  return captures.map((capture, i) => ({
    ...capture,
    audioData: capture.audioData.slice(trimStarts[i], trimStarts[i] + minLength),
    durationSec: minLength / capture.sampleRate,
  }));
}
