/**
 * Sound Power and Directivity Index vs Frequency — AN69 standard curves.
 */

import { useEffect, useRef } from 'react';
import Plotly from 'plotly.js-dist-min';
import type { DirectionalSpectrum } from '../../audio/spectrum.ts';
import {
  computeSoundPowerSpectrum,
  computeDirectivityIndexSpectrum,
} from '../../audio/spectrum.ts';

interface DirectivityIndexPlotProps {
  spectra: DirectionalSpectrum[];
  freqMin?: number;
  freqMax?: number;
}

export function DirectivityIndexPlot({
  spectra,
  freqMin = 20,
  freqMax = 20000,
}: DirectivityIndexPlotProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current || spectra.length === 0) return;

    const sp = computeSoundPowerSpectrum(spectra);
    const di = computeDirectivityIndexSpectrum(spectra);
    if (!sp || !di) return;

    const mask = Array.from(sp.frequencies).map((f) => f >= freqMin && f <= freqMax);
    const freqs = Array.from(sp.frequencies).filter((_, i) => mask[i]);

    // On-axis reference
    const onAxis = spectra.find((s) => s.elevationDeg === 0 && s.azimuthDeg === 0);
    const onAxisData = onAxis
      ? Array.from(onAxis.spectrum.magnitudeDb).filter((_, i) => mask[i])
      : null;

    const data: Plotly.Data[] = [];

    if (onAxisData) {
      data.push({
        type: 'scatter',
        mode: 'lines',
        name: 'On-Axis',
        x: freqs,
        y: onAxisData,
        line: { color: '#ef4444', width: 2 },
        yaxis: 'y',
        hovertemplate: 'On-Axis: %{y:.1f} dB @ %{x:.0f} Hz<extra></extra>',
      } as Plotly.Data);
    }

    data.push({
      type: 'scatter',
      mode: 'lines',
      name: 'Sound Power',
      x: freqs,
      y: Array.from(sp.magnitudeDb).filter((_, i) => mask[i]),
      line: { color: '#3b82f6', width: 2 },
      yaxis: 'y',
      hovertemplate: 'Sound Power: %{y:.1f} dB @ %{x:.0f} Hz<extra></extra>',
    } as Plotly.Data);

    data.push({
      type: 'scatter',
      mode: 'lines',
      name: 'Directivity Index',
      x: freqs,
      y: Array.from(di.magnitudeDb).filter((_, i) => mask[i]),
      line: { color: '#22c55e', width: 2 },
      yaxis: 'y2',
      hovertemplate: 'DI: %{y:.1f} dB @ %{x:.0f} Hz<extra></extra>',
    } as Plotly.Data);

    const layout: Partial<Plotly.Layout> = {
      title: {
        text: 'Sound Power & Directivity Index',
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
        title: { text: 'SPL (dB)', font: { color: '#3b82f6' } },
        color: '#9ca3af',
        gridcolor: '#374151',
        side: 'left',
      },
      yaxis2: {
        title: { text: 'DI (dB)', font: { color: '#22c55e' } },
        color: '#9ca3af',
        overlaying: 'y',
        side: 'right',
        showgrid: false,
      },
      paper_bgcolor: '#111827',
      plot_bgcolor: '#1f2937',
      font: { color: '#e5e7eb' },
      legend: {
        bgcolor: 'rgba(17,24,39,0.8)',
        font: { color: '#e5e7eb' },
        orientation: 'h',
        y: -0.15,
      },
      margin: { l: 60, r: 60, t: 40, b: 70 },
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
  }, [spectra, freqMin, freqMax]);

  if (spectra.length === 0) {
    return (
      <div className="text-center text-gray-500 py-8 text-sm">
        No spectral data — capture measurements first
      </div>
    );
  }

  return <div ref={containerRef} className="w-full" style={{ minHeight: 380 }} />;
}
