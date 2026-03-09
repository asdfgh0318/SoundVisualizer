/**
 * Polar plot at a user-selected frequency — uses Plotly polar chart.
 * Shows radiation pattern for a specific frequency like AN69 polar plots.
 */

import { useEffect, useRef } from 'react';
import Plotly from 'plotly.js-dist-min';
import type { DirectionalSpectrum } from '../../audio/spectrum.ts';
import { splAtFrequency } from '../../audio/spectrum.ts';
import { ELEVATION_ANGLES } from '../../types/index.ts';

interface PolarAtFrequencyProps {
  spectra: DirectionalSpectrum[];
  frequencyHz: number;
}

const ELEV_COLORS: Record<number, string> = {
  [-90]: '#6366f1',
  [-45]: '#3b82f6',
  [0]: '#ef4444',
  [45]: '#22c55e',
  [90]: '#eab308',
};

export function PolarAtFrequency({ spectra, frequencyHz }: PolarAtFrequencyProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current || spectra.length === 0) return;

    const data: Plotly.Data[] = [];

    for (const elev of ELEVATION_ANGLES) {
      const atElev = spectra
        .filter((s) => s.elevationDeg === elev)
        .sort((a, b) => a.azimuthDeg - b.azimuthDeg);

      if (atElev.length === 0) continue;

      const theta = atElev.map((s) => s.azimuthDeg);
      const r = atElev.map((s) => {
        const spl = splAtFrequency(s.spectrum, frequencyHz);
        return isFinite(spl) ? spl : -100;
      });

      data.push({
        type: 'scatterpolar',
        mode: 'lines+markers',
        name: `${elev > 0 ? '+' : ''}${elev}° elev`,
        theta: [...theta, theta[0]], // close the loop
        r: [...r, r[0]],
        line: { color: ELEV_COLORS[elev] ?? '#9ca3af', width: 2 },
        marker: { size: 4 },
        hovertemplate: `Az: %{theta}°, ${elev}° elev<br>%{r:.1f} dB<extra></extra>`,
      } as Plotly.Data);
    }

    const layout: Partial<Plotly.Layout> = {
      title: {
        text: `Polar Pattern @ ${frequencyHz >= 1000 ? (frequencyHz / 1000).toFixed(1) + ' kHz' : frequencyHz + ' Hz'}`,
        font: { color: '#e5e7eb', size: 14 },
      },
      polar: {
        bgcolor: '#1f2937',
        angularaxis: {
          direction: 'clockwise',
          rotation: 90,
          color: '#9ca3af',
          gridcolor: '#374151',
          linecolor: '#374151',
        },
        radialaxis: {
          color: '#9ca3af',
          gridcolor: '#374151',
          angle: 90,
          ticksuffix: ' dB',
        },
      },
      paper_bgcolor: '#111827',
      font: { color: '#e5e7eb' },
      legend: {
        bgcolor: 'rgba(17,24,39,0.8)',
        font: { color: '#e5e7eb', size: 10 },
      },
      margin: { l: 40, r: 40, t: 50, b: 30 },
      showlegend: true,
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
  }, [spectra, frequencyHz]);

  if (spectra.length === 0) {
    return (
      <div className="text-center text-gray-500 py-8 text-sm">
        No spectral data — capture measurements first
      </div>
    );
  }

  return <div ref={containerRef} className="w-full" style={{ minHeight: 420 }} />;
}
