import { useEffect, useMemo, useState } from 'react';
import { api } from '../../api/client';
import type { AcousticInPoint, Key, MergedPWMPoint } from '../../api/types';

// Series #0 is always the indigo base (the currently selected point); extras cycle the rest.
export const SERIES_PALETTE = ['#818cf8', '#f472b6', '#34d399', '#fb923c', '#22d3ee', '#a78bfa', '#facc15'];

/** A data series to overlay = one (key, PWM point). Mics are matched across
 *  series by elevation. Shared by the FFT and Polar tabs. */
export interface CompareSeries {
  id: string; // `${keySlug}::${pointId}`
  keySlug: string;
  pointId: string;
  pwm_us: number;
  acoustic: AcousticInPoint[];
  label: string;
  color: string;
}

export interface CompareSeriesApi {
  series: CompareSeries[];
  keys: Key[];
  labelForKey: (slug: string) => string;
  addSeries: (s: CompareSeries) => void;
  removeSeries: (id: string) => void;
}

/** Manages the overlay series list: base (the selected point) + user-added extras,
 *  with cycled colors and human labels resolved from the key list. Lifted to the
 *  Results level so the comparison persists across the FFT/Polar tabs. */
export function useCompareSeries(keySlug: string, point: MergedPWMPoint | null): CompareSeriesApi {
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

  const series = useMemo<CompareSeries[]>(() => {
    if (!point) return [];
    const base: CompareSeries = {
      id: `${keySlug}::${point.id}`,
      keySlug,
      pointId: point.id,
      pwm_us: point.pwm_us,
      acoustic: point.acoustic,
      label: `${labelForKey(keySlug)} · ${point.pwm_us}µs`,
      color: SERIES_PALETTE[0],
    };
    const rest = extra
      .filter((s) => s.id !== base.id)
      .map((s, i) => ({ ...s, color: SERIES_PALETTE[(i + 1) % SERIES_PALETTE.length] }));
    return [base, ...rest];
  }, [keySlug, point, extra, labelForKey]);

  const addSeries = (s: CompareSeries) =>
    setExtra((prev) => (prev.some((e) => e.id === s.id) ? prev : [...prev, s]));
  const removeSeries = (id: string) => setExtra((prev) => prev.filter((e) => e.id !== id));

  return { series, keys, labelForKey, addSeries, removeSeries };
}

/** Cross-key series picker: key → PWM point → add. Shows active series as chips. */
export function SeriesPicker({
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
      <div className="text-xs uppercase tracking-wide text-gray-400">Compare configs (overlay)</div>

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
