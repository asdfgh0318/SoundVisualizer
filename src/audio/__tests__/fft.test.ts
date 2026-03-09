import { describe, it, expect } from 'vitest';
import { fft, nextPow2 } from '../fft.ts';

describe('FFT', () => {
  it('returns nextPow2 correctly', () => {
    expect(nextPow2(1)).toBe(1);
    expect(nextPow2(3)).toBe(4);
    expect(nextPow2(1000)).toBe(1024);
    expect(nextPow2(1024)).toBe(1024);
  });

  it('throws on non-power-of-2', () => {
    const re = new Float64Array(3);
    const im = new Float64Array(3);
    expect(() => fft(re, im)).toThrow();
  });

  it('handles length-1 input', () => {
    const re = new Float64Array([5]);
    const im = new Float64Array([0]);
    fft(re, im);
    expect(re[0]).toBe(5);
  });

  it('correctly transforms a DC signal', () => {
    const n = 8;
    const re = new Float64Array(n).fill(1);
    const im = new Float64Array(n).fill(0);
    fft(re, im);
    // DC bin should be n, all others 0
    expect(re[0]).toBeCloseTo(n, 10);
    for (let i = 1; i < n; i++) {
      expect(Math.abs(re[i])).toBeLessThan(1e-10);
      expect(Math.abs(im[i])).toBeLessThan(1e-10);
    }
  });

  it('correctly transforms a single-frequency sine', () => {
    const n = 64;
    const re = new Float64Array(n);
    const im = new Float64Array(n);
    const k = 3; // frequency bin
    for (let i = 0; i < n; i++) {
      re[i] = Math.cos((2 * Math.PI * k * i) / n);
    }
    fft(re, im);
    // Expect energy at bin k and bin n-k
    const mag = Math.sqrt(re[k] * re[k] + im[k] * im[k]);
    expect(mag).toBeCloseTo(n / 2, 5);
  });
});
