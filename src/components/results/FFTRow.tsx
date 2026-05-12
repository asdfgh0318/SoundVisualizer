import { useEffect, useMemo, useState } from 'react';
import { api } from '../../api/client';
import type { AcousticInPoint, FFTResponse, FFTSettings } from '../../api/types';
import { PlotlyChart } from '../ui/PlotlyChart';

interface Props {
  keySlug: string;
  acoustic: AcousticInPoint;
  settings: FFTSettings;
}

export function FFTRow({ keySlug, acoustic, settings }: Props) {
  const [resp, setResp] = useState<FFTResponse | null>(null);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let cancelled = false;
    setResp(null);
    setError(null);
    api.getFFT(keySlug, acoustic.id, settings).then(
      (r) => !cancelled && setResp(r),
      (e) => !cancelled && setError(e),
    );
    return () => { cancelled = true; };
  }, [keySlug, acoustic.id, settings.window, settings.size, settings.overlap]);

  const trace = useMemo(() => {
    if (!resp) return null;
    // Drop the DC bin (frequencies[0] = 0) — log axis can't handle 0.
    const freqs = resp.frequencies.slice(1);
    const mags = resp.magnitudes_db.slice(1);
    return [
      {
        x: freqs,
        y: mags,
        type: 'scatter' as const,
        mode: 'lines' as const,
        line: { color: '#818cf8', width: 1 },
        hovertemplate: '%{x:.0f} Hz<br>%{y:.1f} dB<extra></extra>',
      },
    ];
  }, [resp]);

  const layout = useMemo(
    () => ({
      autosize: true,
      height: 160,
      margin: { l: 50, r: 12, t: 8, b: 32 },
      paper_bgcolor: 'rgba(0,0,0,0)',
      plot_bgcolor: 'rgba(0,0,0,0)',
      xaxis: {
        type: 'log' as const,
        range: [Math.log10(20), Math.log10(24000)],
        gridcolor: '#374151',
        zerolinecolor: '#374151',
        tickfont: { color: '#9ca3af', size: 10 },
      },
      yaxis: {
        gridcolor: '#374151',
        zerolinecolor: '#374151',
        tickfont: { color: '#9ca3af', size: 10 },
        title: { text: 'dB', font: { color: '#9ca3af', size: 10 } },
      },
      showlegend: false,
    }),
    [],
  );

  const elev = acoustic.elevation_deg;
  const elevLabel = elev > 0 ? `+${elev}°` : `${elev}°`;

  return (
    <div className="grid grid-cols-[120px_1fr] items-center gap-4 bg-gray-900/40 border border-gray-700 rounded-md p-3">
      <div>
        <div className="text-2xl font-mono font-bold text-gray-100">{elevLabel}</div>
        <div className="text-[11px] text-gray-500 font-mono mt-0.5">{acoustic.mic_serial}</div>
        {resp?.calibrated && (
          <span className="inline-block mt-1 text-[10px] uppercase tracking-wide text-emerald-400">
            calibrated
          </span>
        )}
      </div>
      <div className="min-h-[160px]">
        {error && <div className="text-xs text-red-400 p-2">FFT error: {error.message}</div>}
        {!error && !resp && (
          <div className="text-xs text-gray-500 italic p-2">Computing…</div>
        )}
        {trace && <PlotlyChart data={trace} layout={layout} className="w-full h-[160px]" />}
      </div>
    </div>
  );
}
