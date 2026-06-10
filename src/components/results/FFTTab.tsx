import type { Data, Layout } from 'plotly.js';
import { useEffect, useMemo, useState } from 'react';
import { api } from '../../api/client';
import type { AcousticInPoint, FFTResponse, FFTSettings, Key, MergedPWMPoint } from '../../api/types';
import { PlotlyChart } from '../ui/PlotlyChart';
import { FFTSettingsBar } from './FFTSettingsPopover';

interface Props {
  keySlug: string;
  point: MergedPWMPoint;
}

const DEFAULT_SETTINGS: FFTSettings = { window: 'hann', size: 4096, overlap: 0.5 };
// Series #0 is always the indigo base (the currently selected point); extras cycle the rest.
const PALETTE = ['#818cf8', '#f472b6', '#34d399', '#fb923c', '#22d3ee', '#a78bfa', '#facc15'];

/** A data series to overlay = one (key, PWM point). Its mics are matched to
 *  other series by elevation, so each mic-position row shows one line per series. */
interface CompareSeries {
  id: string; // `${keySlug}::${pointId}`
  keySlug: string;
  pointId: string;
  pwm_us: number;
  acoustic: AcousticInPoint[];
  label: string;
  color: string;
}

export function FFTTab({ keySlug, point }: Props) {
  const [settings, setSettings] = useState<FFTSettings>(DEFAULT_SETTINGS);
  const [extra, setExtra] = useState<CompareSeries[]>([]);
  const [keys, setKeys] = useState<Key[]>([]);

  useEffect(() => {
    api.listKeys().then(setKeys, () => setKeys([]));
  }, []);

  const labelForKey = useMemo(() => {
    const bySlug = new Map(keys.map((k) => [k.slug, k]));
    return (slug: string): string => {
      const k = bySlug.get(slug);
      if (!k) return slug.split('__')[1] ?? slug; // fallback: propeller part of the slug
      const shroud = k.shroud && k.shroud !== 'none' ? ` [${k.shroud}]` : '';
      return `${k.propeller}${shroud}`.trim() || k.motor || slug;
    };
  }, [keys]);

  // Series #0 = the currently selected point; extras follow with cycled colors.
  const series = useMemo<CompareSeries[]>(() => {
    const base: CompareSeries = {
      id: `${keySlug}::${point.id}`,
      keySlug,
      pointId: point.id,
      pwm_us: point.pwm_us,
      acoustic: point.acoustic,
      label: `${labelForKey(keySlug)} · ${point.pwm_us}µs`,
      color: PALETTE[0],
    };
    const rest = extra
      .filter((s) => s.id !== base.id)
      .map((s, i) => ({ ...s, color: PALETTE[(i + 1) % PALETTE.length] }));
    return [base, ...rest];
  }, [keySlug, point, extra, labelForKey]);

  // Union of elevations across all series → one row each, sorted top→bottom.
  const elevations = useMemo(() => {
    const set = new Set<number>();
    series.forEach((s) => s.acoustic.forEach((a) => set.add(a.elevation_deg)));
    return [...set].sort((a, b) => b - a);
  }, [series]);

  const comparing = series.length > 1;

  return (
    <div className="space-y-4">
      <FFTSettingsBar settings={settings} onChange={setSettings} />

      <SeriesPicker
        keys={keys}
        series={series}
        baseId={series[0]?.id}
        labelForKey={labelForKey}
        onAdd={(s) => setExtra((prev) => (prev.some((e) => e.id === s.id) ? prev : [...prev, s]))}
        onRemove={(id) => setExtra((prev) => prev.filter((e) => e.id !== id))}
      />

      <div className="space-y-3">
        {elevations.length === 0 && (
          <div className="text-sm text-gray-400 italic">No acoustic measurements at this point.</div>
        )}
        {elevations.map((elev) => (
          <OverlayRow key={elev} elevation={elev} series={series} settings={settings} showLegend={comparing} />
        ))}
      </div>
    </div>
  );
}

/** One mic-position row: overlays each series' spectrum at this elevation. */
function OverlayRow({
  elevation,
  series,
  settings,
  showLegend,
}: {
  elevation: number;
  series: CompareSeries[];
  settings: FFTSettings;
  showLegend: boolean;
}) {
  const members = useMemo(
    () =>
      series
        .map((s) => ({ s, a: s.acoustic.find((a) => a.elevation_deg === elevation) }))
        .filter((m): m is { s: CompareSeries; a: AcousticInPoint } => m.a !== undefined),
    [series, elevation],
  );

  const [resps, setResps] = useState<Record<string, FFTResponse>>({});
  const [error, setError] = useState<string | null>(null);

  const memberKey = members.map((m) => m.a.id).join(',');
  useEffect(() => {
    let cancelled = false;
    setError(null);
    members.forEach(({ s, a }) => {
      api.getFFT(s.keySlug, a.id, settings).then(
        (r) => !cancelled && setResps((prev) => ({ ...prev, [a.id]: r })),
        (e: Error) => !cancelled && setError(e.message),
      );
    });
    return () => { cancelled = true; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [memberKey, settings.window, settings.size, settings.overlap]);

  const traces = useMemo<Data[]>(
    () =>
      members.map(({ s, a }): Data => {
        const r = resps[a.id];
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
    [members, resps],
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
        {error && <div className="text-xs text-red-400 p-2">FFT error: {error}</div>}
        {!error && <PlotlyChart data={traces} layout={layout} className="w-full" />}
      </div>
    </div>
  );
}

/** Cross-key series picker: key → PWM point → add. Shows active series as chips. */
function SeriesPicker({
  keys,
  series,
  baseId,
  labelForKey,
  onAdd,
  onRemove,
}: {
  keys: Key[];
  series: CompareSeries[];
  baseId: string | undefined;
  labelForKey: (slug: string) => string;
  onAdd: (s: CompareSeries) => void;
  onRemove: (id: string) => void;
}) {
  const [selKey, setSelKey] = useState('');
  const [points, setPoints] = useState<MergedPWMPoint[]>([]);
  const [selPoint, setSelPoint] = useState('');

  useEffect(() => {
    if (!selKey) { setPoints([]); setSelPoint(''); return; }
    let cancelled = false;
    api.listPWMPoints(selKey).then(
      (p) => { if (!cancelled) { setPoints(p); setSelPoint(p[0]?.id ?? ''); } },
      () => !cancelled && setPoints([]),
    );
    return () => { cancelled = true; };
  }, [selKey]);

  const add = () => {
    const p = points.find((x) => x.id === selPoint);
    if (!selKey || !p) return;
    onAdd({
      id: `${selKey}::${p.id}`,
      keySlug: selKey,
      pointId: p.id,
      pwm_us: p.pwm_us,
      acoustic: p.acoustic,
      label: `${labelForKey(selKey)} · ${p.pwm_us}µs`,
      color: '',
    });
  };

  return (
    <div className="bg-gray-800 border border-gray-700 rounded-md p-3 space-y-3">
      <div className="text-xs uppercase tracking-wide text-gray-400">Compare configs (overlay on each mic row)</div>

      <div className="flex flex-wrap items-end gap-2">
        <label className="block">
          <span className="text-[11px] text-gray-500">Config</span>
          <select className="input mt-1 w-56" value={selKey} onChange={(e) => setSelKey(e.target.value)}>
            <option value="">— pick a config —</option>
            {keys.map((k) => (
              <option key={k.slug} value={k.slug}>
                {k.motor} · {k.propeller}{k.shroud && k.shroud !== 'none' ? ` · ${k.shroud}` : ''}
              </option>
            ))}
          </select>
        </label>
        <label className="block">
          <span className="text-[11px] text-gray-500">PWM point</span>
          <select
            className="input mt-1 w-40"
            value={selPoint}
            onChange={(e) => setSelPoint(e.target.value)}
            disabled={!points.length}
          >
            {!points.length && <option value="">—</option>}
            {points.map((p) => (
              <option key={p.id} value={p.id}>{p.pwm_us} µs</option>
            ))}
          </select>
        </label>
        <button
          onClick={add}
          disabled={!selPoint}
          className="text-sm font-medium rounded px-3 py-2 border border-gray-600 text-gray-200 hover:border-indigo-500 hover:text-white disabled:opacity-40 disabled:cursor-not-allowed"
        >
          + Add series
        </button>
      </div>

      <div className="flex flex-wrap gap-2">
        {series.map((s) => (
          <span
            key={s.id}
            className="inline-flex items-center gap-2 text-xs rounded-full pl-2 pr-1 py-1 bg-gray-900/60 border border-gray-700"
          >
            <span className="inline-block w-2.5 h-2.5 rounded-full" style={{ background: s.color }} />
            <span className="text-gray-200">{s.label}</span>
            {s.id === baseId ? (
              <span className="text-[10px] text-gray-500 uppercase px-1">base</span>
            ) : (
              <button
                onClick={() => onRemove(s.id)}
                className="text-gray-500 hover:text-red-400 px-1"
                aria-label={`Remove ${s.label}`}
              >
                ✕
              </button>
            )}
          </span>
        ))}
      </div>
    </div>
  );
}
