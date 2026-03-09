/**
 * Spectral analysis module — computes magnitude spectrum from raw audio.
 * Used by all frequency-dependent visualizations.
 */

import { fft, nextPow2 } from './fft.ts';
import type { Measurement } from '../types/index.ts';

export interface SpectrumResult {
  /** Frequency values in Hz for each bin (length = fftSize/2 + 1). */
  frequencies: Float64Array;
  /** Magnitude in dB (relative to full scale) for each bin. */
  magnitudeDb: Float64Array;
}

export interface DirectionalSpectrum {
  azimuthDeg: number;
  elevationDeg: number;
  spectrum: SpectrumResult;
}

/**
 * Apply a Hann window to samples in-place.
 */
function applyHannWindow(samples: Float64Array): void {
  const n = samples.length;
  for (let i = 0; i < n; i++) {
    const w = 0.5 * (1 - Math.cos((2 * Math.PI * i) / (n - 1)));
    samples[i] *= w;
  }
}

/**
 * Compute the magnitude spectrum of a mono audio buffer.
 * Returns frequencies (Hz) and magnitudes (dBFS).
 */
export function computeSpectrum(
  samples: Float32Array,
  sampleRate: number,
  fftSize?: number,
): SpectrumResult {
  if (samples.length === 0) {
    return { frequencies: new Float64Array(0), magnitudeDb: new Float64Array(0) };
  }

  // Cap FFT size at 16384 for performance — sufficient for ~3 Hz resolution at 48kHz
  const MAX_FFT = 16384;
  const raw = fftSize ?? nextPow2(Math.min(samples.length, MAX_FFT));
  const n = Math.min(raw, MAX_FFT);
  const re = new Float64Array(n);
  const im = new Float64Array(n);

  // Copy samples (truncated to FFT window) and zero-pad
  const copyLen = Math.min(samples.length, n);
  for (let i = 0; i < copyLen; i++) {
    re[i] = samples[i];
  }

  applyHannWindow(re);
  fft(re, im);

  // Compute magnitude in dB for positive frequencies
  const numBins = n / 2 + 1;
  const frequencies = new Float64Array(numBins);
  const magnitudeDb = new Float64Array(numBins);
  const binWidth = sampleRate / n;

  for (let i = 0; i < numBins; i++) {
    frequencies[i] = i * binWidth;
    const mag = Math.sqrt(re[i] * re[i] + im[i] * im[i]) / (n / 2);
    magnitudeDb[i] = mag > 0 ? 20 * Math.log10(mag) : -Infinity;
  }

  return { frequencies, magnitudeDb };
}

/**
 * Compute SPL (dB) at a specific frequency from a spectrum.
 * Finds the nearest bin.
 */
export function splAtFrequency(spectrum: SpectrumResult, freqHz: number): number {
  const binWidth = spectrum.frequencies[1] - spectrum.frequencies[0];
  if (binWidth <= 0) return -Infinity;
  const bin = Math.round(freqHz / binWidth);
  if (bin < 0 || bin >= spectrum.magnitudeDb.length) return -Infinity;
  return spectrum.magnitudeDb[bin];
}

/**
 * Compute SPL in a 1/N octave band centered at freqHz.
 */
export function splInBand(
  spectrum: SpectrumResult,
  centerFreqHz: number,
  octaveFraction: number = 3,
): number {
  const factor = Math.pow(2, 1 / (2 * octaveFraction));
  const loFreq = centerFreqHz / factor;
  const hiFreq = centerFreqHz * factor;
  const binWidth = spectrum.frequencies[1] - spectrum.frequencies[0];
  if (binWidth <= 0) return -Infinity;

  const loBin = Math.max(0, Math.floor(loFreq / binWidth));
  const hiBin = Math.min(spectrum.magnitudeDb.length - 1, Math.ceil(hiFreq / binWidth));

  let energySum = 0;
  let count = 0;
  for (let i = loBin; i <= hiBin; i++) {
    if (isFinite(spectrum.magnitudeDb[i])) {
      energySum += Math.pow(10, spectrum.magnitudeDb[i] / 10);
      count++;
    }
  }

  if (count === 0) return -Infinity;
  return 10 * Math.log10(energySum / count);
}

/**
 * Compute spectra for all captures across all measurements.
 */
export function computeAllSpectra(
  measurements: Measurement[],
  fftSize?: number,
): DirectionalSpectrum[] {
  const results: DirectionalSpectrum[] = [];
  for (const m of measurements) {
    for (const c of m.captures) {
      results.push({
        azimuthDeg: m.azimuthDeg,
        elevationDeg: c.elevationDeg,
        spectrum: computeSpectrum(c.audioData, c.sampleRate, fftSize),
      });
    }
  }
  return results;
}

/**
 * Compute Sound Power spectrum (energy-averaged across all angles with solid-angle weighting).
 */
export function computeSoundPowerSpectrum(
  spectra: DirectionalSpectrum[],
): SpectrumResult | null {
  if (spectra.length === 0) return null;

  const numBins = spectra[0].spectrum.frequencies.length;
  const frequencies = spectra[0].spectrum.frequencies;
  const magnitudeDb = new Float64Array(numBins);

  for (let bin = 0; bin < numBins; bin++) {
    let weightedSum = 0;
    let totalWeight = 0;

    for (const ds of spectra) {
      const weight = Math.cos((ds.elevationDeg * Math.PI) / 180);
      const absWeight = Math.abs(weight) + 0.01; // small epsilon for poles
      if (isFinite(ds.spectrum.magnitudeDb[bin])) {
        weightedSum += absWeight * Math.pow(10, ds.spectrum.magnitudeDb[bin] / 10);
        totalWeight += absWeight;
      }
    }

    magnitudeDb[bin] = totalWeight > 0
      ? 10 * Math.log10(weightedSum / totalWeight)
      : -Infinity;
  }

  return { frequencies, magnitudeDb };
}

/**
 * Compute Directivity Index spectrum (on-axis minus sound power, in dB).
 */
export function computeDirectivityIndexSpectrum(
  spectra: DirectionalSpectrum[],
): SpectrumResult | null {
  const onAxis = spectra.find(
    (s) => s.elevationDeg === 0 && s.azimuthDeg === 0,
  );
  if (!onAxis) {
    // fallback: average of elevation=0
    const elev0 = spectra.filter((s) => s.elevationDeg === 0);
    if (elev0.length === 0) return null;
  }

  const soundPower = computeSoundPowerSpectrum(spectra);
  if (!soundPower) return null;

  const numBins = soundPower.frequencies.length;
  const frequencies = soundPower.frequencies;
  const magnitudeDb = new Float64Array(numBins);

  // Use on-axis or average of elev=0
  const onAxisSpectrum = onAxis
    ? onAxis.spectrum
    : averageSpectra(spectra.filter((s) => s.elevationDeg === 0).map((s) => s.spectrum));

  if (!onAxisSpectrum) return null;

  for (let bin = 0; bin < numBins; bin++) {
    magnitudeDb[bin] = onAxisSpectrum.magnitudeDb[bin] - soundPower.magnitudeDb[bin];
  }

  return { frequencies, magnitudeDb };
}

/**
 * Energy-average multiple spectra into one.
 */
function averageSpectra(spectra: SpectrumResult[]): SpectrumResult | null {
  if (spectra.length === 0) return null;
  const numBins = spectra[0].frequencies.length;
  const frequencies = spectra[0].frequencies;
  const magnitudeDb = new Float64Array(numBins);

  for (let bin = 0; bin < numBins; bin++) {
    let sum = 0;
    let count = 0;
    for (const s of spectra) {
      if (isFinite(s.magnitudeDb[bin])) {
        sum += Math.pow(10, s.magnitudeDb[bin] / 10);
        count++;
      }
    }
    magnitudeDb[bin] = count > 0 ? 10 * Math.log10(sum / count) : -Infinity;
  }

  return { frequencies, magnitudeDb };
}
