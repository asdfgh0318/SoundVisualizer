/**
 * Contour/Sonogram plot — frequency (X) vs angle (Y) with SPL as color.
 * The flagship AN69 visualization.
 */

import { useEffect, useRef } from 'react';
import Plotly from 'plotly.js-dist-min';
import type { DirectionalSpectrum } from '../../audio/spectrum.ts';

interface ContourPlotProps {
  spectra: DirectionalSpectrum[];
  /** Which angle axis to display: azimuth (horizontal sweep) or elevation */
  angleAxis?: 'azimuth' | 'elevation';
  /** Fixed elevation to filter by when showing azimuth sweep */
  filterElevation?: number;
  /** Fixed azimuth to filter by when showing elevation sweep */
  filterAzimuth?: number;
  /** Min frequency to display (Hz) */
  freqMin?: number;
  /** Max frequency to display (Hz) */
  freqMax?: number;
}

export function ContourPlot({
  spectra,
  angleAxis = 'azimuth',
  filterElevation = 0,
  filterAzimuth,
  freqMin = 20,
  freqMax = 20000,
}: ContourPlotProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current || spectra.length === 0) return;

    // Filter spectra by the fixed axis
    const filtered = angleAxis === 'azimuth'
      ? spectra.filter((s) => s.elevationDeg === filterElevation)
      : spectra.filter((s) => filterAzimuth === undefined || s.azimuthDeg === filterAzimuth);

    if (filtered.length === 0) return;

    const firstFreqs = filtered[0].spectrum.frequencies;
    if (!firstFreqs || firstFreqs.length === 0) return;

    // Sort by angle
    const sorted = [...filtered].sort((a, b) =>
      angleAxis === 'azimuth'
        ? a.azimuthDeg - b.azimuthDeg
        : a.elevationDeg - b.elevationDeg,
    );

    const angles = sorted.map((s) =>
      angleAxis === 'azimuth' ? s.azimuthDeg : s.elevationDeg,
    );

    // Build frequency axis (use log-spaced subset for performance)
    const fullFreqs = sorted[0].spectrum.frequencies;
    const freqIndices: number[] = [];
    const freqLabels: number[] = [];

    for (let i = 0; i < fullFreqs.length; i++) {
      const f = fullFreqs[i];
      if (f >= freqMin && f <= freqMax) {
        freqIndices.push(i);
        freqLabels.push(f);
      }
    }

    // Build Z matrix: z[angle][freq]
    const z = sorted.map((s) =>
      freqIndices.map((fi) => {
        const val = s.spectrum.magnitudeDb[fi];
        return isFinite(val) ? val : -100;
      }),
    );

    // Find SPL range for colorscale
    const allVals = z.flat().filter((v) => v > -100);
    const zMin = allVals.length > 0 ? Math.min(...allVals) : -60;
    const zMax = allVals.length > 0 ? Math.max(...allVals) : 0;

    const data: Plotly.Data[] = [
      {
        type: 'heatmap',
        x: freqLabels,
        y: angles,
        z,
        colorscale: [
          [0, 'rgb(0,0,131)'],
          [0.25, 'rgb(0,60,170)'],
          [0.5, 'rgb(5,255,255)'],
          [0.75, 'rgb(255,255,0)'],
          [1, 'rgb(250,0,0)'],
        ],
        zmin: zMin,
        zmax: zMax,
        colorbar: {
          title: { text: 'dB SPL', side: 'right' },
          thickness: 15,
          len: 0.9,
        },
        hoverongaps: false,
        hovertemplate:
          'Freq: %{x:.0f} Hz<br>Angle: %{y}°<br>SPL: %{z:.1f} dB<extra></extra>',
      } as Plotly.Data,
    ];

    const layout: Partial<Plotly.Layout> = {
      title: {
        text: angleAxis === 'azimuth'
          ? `Directivity Sonogram (Elevation ${filterElevation}°)`
          : 'Directivity Sonogram (Elevation sweep)',
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
        title: { text: angleAxis === 'azimuth' ? 'Azimuth (°)' : 'Elevation (°)' },
        color: '#9ca3af',
        gridcolor: '#374151',
      },
      paper_bgcolor: '#111827',
      plot_bgcolor: '#1f2937',
      font: { color: '#e5e7eb' },
      margin: { l: 60, r: 30, t: 40, b: 50 },
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
  }, [spectra, angleAxis, filterElevation, filterAzimuth, freqMin, freqMax]);

  if (spectra.length === 0) {
    return (
      <div className="text-center text-gray-500 py-8 text-sm">
        No spectral data — capture measurements first
      </div>
    );
  }

  return <div ref={containerRef} className="w-full" style={{ minHeight: 400 }} />;
}
