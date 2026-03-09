/**
 * Multi-curve frequency response plot — overlaid SPL vs frequency
 * for different angles (on-axis, 30° off, 60° off, etc.)
 */

import { useEffect, useRef } from 'react';
import Plotly from 'plotly.js-dist-min';
import type { DirectionalSpectrum, SpectrumResult } from '../../audio/spectrum.ts';
import { computeSoundPowerSpectrum } from '../../audio/spectrum.ts';

interface FrequencyResponsePlotProps {
  spectra: DirectionalSpectrum[];
  /** Which elevation to show curves for */
  elevation?: number;
  /** Show sound power curve */
  showSoundPower?: boolean;
  freqMin?: number;
  freqMax?: number;
}

const ANGLE_COLORS: Record<string, string> = {
  '0': '#ef4444',    // red — on axis
  '15': '#f97316',
  '30': '#eab308',
  '45': '#22c55e',
  '60': '#06b6d4',
  '90': '#3b82f6',
  '120': '#8b5cf6',
  '150': '#d946ef',
  '180': '#6b7280',
};

function getColor(angle: number): string {
  return ANGLE_COLORS[String(Math.abs(angle))] ?? '#9ca3af';
}

/**
 * Smooth a spectrum using 1/N octave smoothing for display.
 */
function smoothSpectrum(spectrum: SpectrumResult, octaveFraction: number = 6): Float64Array {
  const n = spectrum.magnitudeDb.length;
  const smoothed = new Float64Array(n);
  const freqs = spectrum.frequencies;

  for (let i = 0; i < n; i++) {
    const centerFreq = freqs[i];
    if (centerFreq <= 0) {
      smoothed[i] = spectrum.magnitudeDb[i];
      continue;
    }

    const factor = Math.pow(2, 1 / (2 * octaveFraction));
    const loFreq = centerFreq / factor;
    const hiFreq = centerFreq * factor;

    let energySum = 0;
    let count = 0;

    for (let j = 0; j < n; j++) {
      if (freqs[j] >= loFreq && freqs[j] <= hiFreq && isFinite(spectrum.magnitudeDb[j])) {
        energySum += Math.pow(10, spectrum.magnitudeDb[j] / 10);
        count++;
      }
    }

    smoothed[i] = count > 0 ? 10 * Math.log10(energySum / count) : spectrum.magnitudeDb[i];
  }

  return smoothed;
}

export function FrequencyResponsePlot({
  spectra,
  elevation = 0,
  showSoundPower = true,
  freqMin = 20,
  freqMax = 20000,
}: FrequencyResponsePlotProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current || spectra.length === 0) return;

    // Get unique azimuth angles at the selected elevation
    const atElev = spectra.filter((s) => s.elevationDeg === elevation);
    const sorted = [...atElev].sort((a, b) => a.azimuthDeg - b.azimuthDeg);
    if (sorted.length === 0) return;

    const freqs = sorted[0]?.spectrum.frequencies;
    if (!freqs || freqs.length === 0) return;

    // Filter frequency range
    const mask = Array.from(freqs).map((f) => f >= freqMin && f <= freqMax);

    const data: Plotly.Data[] = sorted.map((ds) => {
      const smoothed = smoothSpectrum(ds.spectrum);
      const x = Array.from(freqs).filter((_, i) => mask[i]);
      const y = Array.from(smoothed).filter((_, i) => mask[i]);

      return {
        type: 'scatter',
        mode: 'lines',
        name: `${ds.azimuthDeg}°`,
        x,
        y,
        line: { color: getColor(ds.azimuthDeg), width: ds.azimuthDeg === 0 ? 2.5 : 1.5 },
        hovertemplate: `${ds.azimuthDeg}°: %{y:.1f} dB @ %{x:.0f} Hz<extra></extra>`,
      } as Plotly.Data;
    });

    // Sound Power curve
    if (showSoundPower) {
      const sp = computeSoundPowerSpectrum(spectra);
      if (sp) {
        const smoothed = smoothSpectrum(sp);
        data.push({
          type: 'scatter',
          mode: 'lines',
          name: 'Sound Power',
          x: Array.from(sp.frequencies).filter((_, i) => mask[i]),
          y: Array.from(smoothed).filter((_, i) => mask[i]),
          line: { color: '#ffffff', width: 2, dash: 'dash' },
          hovertemplate: 'Sound Power: %{y:.1f} dB @ %{x:.0f} Hz<extra></extra>',
        } as Plotly.Data);
      }
    }

    const layout: Partial<Plotly.Layout> = {
      title: {
        text: `Frequency Response (Elevation ${elevation}°)`,
        font: { color: '#e5e7eb', size: 14 },
      },
      xaxis: {
        title: { text: 'Frequency (Hz)' },
        type: 'log',
        color: '#9ca3af',
        gridcolor: '#374151',
        range: [Math.log10(freqMin), Math.log10(freqMax)],
      },
      yaxis: {
        title: { text: 'SPL (dB)' },
        color: '#9ca3af',
        gridcolor: '#374151',
      },
      paper_bgcolor: '#111827',
      plot_bgcolor: '#1f2937',
      font: { color: '#e5e7eb' },
      legend: { bgcolor: 'rgba(17,24,39,0.8)', font: { color: '#e5e7eb' } },
      margin: { l: 60, r: 20, t: 40, b: 50 },
    };

    Plotly.react(containerRef.current, data, layout, {
      responsive: true,
      displayModeBar: true,
      modeBarButtonsToRemove: ['lasso2d', 'select2d'],
    });

    return () => {
      if (containerRef.current) {
        Plotly.purge(containerRef.current);
      }
    };
  }, [spectra, elevation, showSoundPower, freqMin, freqMax]);

  if (spectra.length === 0) {
    return (
      <div className="text-center text-gray-500 py-8 text-sm">
        No spectral data — capture measurements first
      </div>
    );
  }

  return <div ref={containerRef} className="w-full" style={{ minHeight: 380 }} />;
}
