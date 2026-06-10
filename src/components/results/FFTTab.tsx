import type { Data, Layout } from 'plotly.js';
import { useEffect, useMemo, useState } from 'react';
import { api } from '../../api/client';
import type { AcousticInPoint, FFTResponse, FFTSettings } from '../../api/types';
import { PlotlyChart } from '../ui/PlotlyChart';
import { type CompareSeries, type CompareSeriesApi, SeriesPicker } from './compareSeries';
import { FFTSettingsBar } from './FFTSettingsPopover';

interface Props {
  compare: CompareSeriesApi;
}

const DEFAULT_SETTINGS: FFTSettings = { window: 'hann', size: 4096, overlap: 0.5 };

export function FFTTab({ compare }: Props) {
  const [settings, setSettings] = useState<FFTSettings>(DEFAULT_SETTINGS);
  const { series, keys, labelForKey, addSeries, removeSeries } = compare;

  // Fetch every series' mics centrally (one cache), so rows are pure renderers
  // and we can report calibration state across the whole comparison.
  const [ffts, setFfts] = useState<Record<string, FFTResponse>>({});
  const [error, setError] = useState<string | null>(null);

  const allAcoustic = useMemo(
    () => series.flatMap((s) => s.acoustic.map((a) => ({ keySlug: s.keySlug, id: a.id }))),
    [series],
  );
  const allIdsKey = allAcoustic.map((a) => a.id).join(',');

  useEffect(() => {
    let cancelled = false;
    setError(null);
    Promise.all(
      allAcoustic.map((a) =>
        api.getFFT(a.keySlug, a.id, settings).then((r): [string, FFTResponse] => [a.id, r]),
      ),
    ).then(
      (entries) => !cancelled && setFfts(Object.fromEntries(entries)),
      (e: Error) => !cancelled && setError(e.message),
    );
    return () => { cancelled = true; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [allIdsKey, settings.window, settings.size, settings.overlap]);

  // Union of elevations across all series → one row each, sorted top→bottom.
  const elevations = useMemo(() => {
    const set = new Set<number>();
    series.forEach((s) => s.acoustic.forEach((a) => set.add(a.elevation_deg)));
    return [...set].sort((a, b) => b - a);
  }, [series]);

  const fetched = allAcoustic.filter((a) => ffts[a.id]);
  const allCalibrated = fetched.length > 0 && fetched.every((a) => ffts[a.id]?.calibrated);
  const mixedCalibration =
    fetched.some((a) => ffts[a.id]?.calibrated) && !allCalibrated;
  const comparing = series.length > 1;

  return (
    <div className="space-y-4">
      <FFTSettingsBar settings={settings} onChange={setSettings} />

      <SeriesPicker
        keys={keys}
        series={series}
        baseId={series[0]?.id}
        labelForKey={labelForKey}
        onAdd={addSeries}
        onRemove={removeSeries}
      />

      {error && <div className="text-sm text-red-400">FFT error: {error}</div>}

      {mixedCalibration && (
        <div className="text-xs text-amber-400 bg-amber-500/10 border border-amber-500/30 rounded-md p-2">
          ⚠ Mixing calibrated (dB SPL) and uncalibrated (dBFS) series — absolute levels aren't comparable across these lines.
        </div>
      )}

      <div className="space-y-3">
        {elevations.length === 0 && (
          <div className="text-sm text-gray-400 italic">No acoustic measurements at this point.</div>
        )}
        {elevations.map((elev) => (
          <OverlayRow key={elev} elevation={elev} series={series} ffts={ffts} showLegend={comparing} />
        ))}
      </div>
    </div>
  );
}

/** One mic-position row: overlays each series' spectrum at this elevation, from
 *  the shared FFT cache. Pure renderer — no fetching. */
function OverlayRow({
  elevation,
  series,
  ffts,
  showLegend,
}: {
  elevation: number;
  series: CompareSeries[];
  ffts: Record<string, FFTResponse>;
  showLegend: boolean;
}) {
  const members = useMemo(
    () =>
      series
        .map((s) => ({ s, a: s.acoustic.find((a) => a.elevation_deg === elevation) }))
        .filter((m): m is { s: CompareSeries; a: AcousticInPoint } => m.a !== undefined),
    [series, elevation],
  );

  const traces = useMemo<Data[]>(
    () =>
      members.map(({ s, a }): Data => {
        const r = ffts[a.id];
        return {
          type: 'scatter',
          mode: 'lines',
          name: s.label,
          x: r ? r.frequencies.slice(1) : [],
          y: r ? r.magnitudes_db.slice(1) : [],
          line: { color: s.color, width: 1.3 },
          hovertemplate: `${s.label}<br>%{x:.0f} Hz<br>%{y:.1f} dB<extra></extra>`,
        };
      }),
    [members, ffts],
  );

  const layout = useMemo<Partial<Layout>>(
    () => ({
      autosize: true,
      height: showLegend ? 210 : 170,
      margin: { l: 50, r: 12, t: showLegend ? 28 : 8, b: 32 },
      paper_bgcolor: 'rgba(0,0,0,0)',
      plot_bgcolor: 'rgba(0,0,0,0)',
      xaxis: {
        type: 'log',
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
      showlegend: showLegend,
      legend: { orientation: 'h', x: 0, y: 1.18, font: { color: '#d1d5db', size: 10 }, bgcolor: 'rgba(0,0,0,0)' },
    }),
    [showLegend],
  );

  const elevLabel = elevation > 0 ? `+${elevation}°` : `${elevation}°`;

  return (
    <div className="grid grid-cols-[120px_1fr] items-center gap-4 bg-gray-900/40 border border-gray-700 rounded-md p-3">
      <div>
        <div className="text-2xl font-mono font-bold text-gray-100">{elevLabel}</div>
        <div className="text-[11px] text-gray-500 mt-0.5">{members.length} series</div>
      </div>
      <div className="min-h-[170px]">
        <PlotlyChart data={traces} layout={layout} className="w-full" />
      </div>
    </div>
  );
}
