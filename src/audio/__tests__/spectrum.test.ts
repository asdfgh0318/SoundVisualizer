import { describe, it, expect } from 'vitest';
import { computeSpectrum, splAtFrequency } from '../spectrum.ts';

describe('Spectrum analysis', () => {
  it('computes spectrum of silence', () => {
    const samples = new Float32Array(1024);
    const result = computeSpectrum(samples, 48000);
    // All bins should be -Infinity for silence
    for (let i = 0; i < result.magnitudeDb.length; i++) {
      expect(result.magnitudeDb[i]).toBe(-Infinity);
    }
  });

  it('detects a 1kHz sine at the right frequency bin', () => {
    const sampleRate = 48000;
    const freq = 1000;
    const n = 4096;
    const samples = new Float32Array(n);
    for (let i = 0; i < n; i++) {
      samples[i] = Math.sin((2 * Math.PI * freq * i) / sampleRate);
    }

    const result = computeSpectrum(samples, sampleRate, n);

    // Find the bin with max magnitude
    let maxBin = 0;
    let maxVal = -Infinity;
    for (let i = 1; i < result.magnitudeDb.length; i++) {
      if (result.magnitudeDb[i] > maxVal) {
        maxVal = result.magnitudeDb[i];
        maxBin = i;
      }
    }

    const peakFreq = result.frequencies[maxBin];
    expect(peakFreq).toBeCloseTo(freq, -1); // within ~10Hz
  });

  it('splAtFrequency returns a reasonable value for a known signal', () => {
    const sampleRate = 48000;
    const freq = 1000;
    const n = 4096;
    const samples = new Float32Array(n);
    for (let i = 0; i < n; i++) {
      samples[i] = 0.5 * Math.sin((2 * Math.PI * freq * i) / sampleRate);
    }

    const spectrum = computeSpectrum(samples, sampleRate, n);
    const spl = splAtFrequency(spectrum, freq);

    // Should be a finite negative value (since amplitude < 1)
    expect(isFinite(spl)).toBe(true);
    expect(spl).toBeLessThan(0);
    expect(spl).toBeGreaterThan(-40);
  });

  it('frequencies array starts at 0 and ends at Nyquist', () => {
    const sampleRate = 48000;
    const n = 1024;
    const samples = new Float32Array(n);
    const result = computeSpectrum(samples, sampleRate, n);

    expect(result.frequencies[0]).toBe(0);
    expect(result.frequencies[result.frequencies.length - 1]).toBeCloseTo(sampleRate / 2, 0);
  });
});
