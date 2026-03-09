import { describe, it, expect } from 'vitest';
import { computeRms, computeSplDb } from '../spl.ts';

describe('SPL computation', () => {
  it('returns 0 RMS for empty array', () => {
    expect(computeRms(new Float32Array(0))).toBe(0);
  });

  it('returns -Infinity dB for silence', () => {
    expect(computeSplDb(new Float32Array(100))).toBe(-Infinity);
  });

  it('returns 0 dB for full-scale DC', () => {
    const samples = new Float32Array(1000).fill(1);
    expect(computeSplDb(samples)).toBeCloseTo(0, 1);
  });

  it('computes correct RMS for a known signal', () => {
    // RMS of a sine wave with amplitude 1 is 1/sqrt(2) ≈ 0.7071
    const N = 48000;
    const samples = new Float32Array(N);
    for (let i = 0; i < N; i++) {
      samples[i] = Math.sin((2 * Math.PI * 1000 * i) / N);
    }
    expect(computeRms(samples)).toBeCloseTo(1 / Math.sqrt(2), 2);
  });

  it('returns ~-3 dB for a unit sine wave', () => {
    // 20*log10(1/sqrt(2)) ≈ -3.01 dB
    const N = 48000;
    const samples = new Float32Array(N);
    for (let i = 0; i < N; i++) {
      samples[i] = Math.sin((2 * Math.PI * 1000 * i) / N);
    }
    expect(computeSplDb(samples)).toBeCloseTo(-3.01, 1);
  });

  it('half amplitude gives ~-9 dB relative to full scale', () => {
    // 20*log10(0.5/sqrt(2)) = 20*log10(0.5) + 20*log10(1/sqrt(2)) ≈ -6.02 + -3.01 ≈ -9.03
    const N = 48000;
    const samples = new Float32Array(N);
    for (let i = 0; i < N; i++) {
      samples[i] = 0.5 * Math.sin((2 * Math.PI * 1000 * i) / N);
    }
    expect(computeSplDb(samples)).toBeCloseTo(-9.03, 1);
  });
});
