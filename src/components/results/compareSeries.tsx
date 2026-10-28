import { useEffect, useMemo, useState } from 'react';
import { api } from '../../api/client';
import type { AcousticInPoint, Key, MergedPWMPoint, UnderlyingCapture } from '../../api/types';
import { BASE_HELP } from '../../content/parameterHelp';
import { InfoToggle } from '../ui/InfoToggle';
import { keyLabel, seriesLabel } from './keyLabel';

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
  /** Per-capture mic lists; carries the repeat index for the Polar tab's repeat view. */
  underlying: UnderlyingCapture[];
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
      return seriesLabel(k);
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
      underlying: point.underlying,
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

const localDay = (iso: string) => new Date(iso).toLocaleDateString('sv');

/** One series per base at `pwmUs`, holding only the captures of that base's most recent day
 *  within [from, to]; captures from other days are dropped even when they merged into the
 *  same point, so no curve mixes days. */
async function seriesForDays(
  keys: Key[],
  from: string,
  to: string,
  pwmUs: number,
  labelForKey: (slug: string) => string,
): Promise<CompareSeries[]> {
  const perKey = await Promise.all(
    keys.map(async (k) => {
      const points = await api.listPWMPoints(k.slug).catch(() => [] as MergedPWMPoint[]);
      return points
        .filter((p) => p.pwm_us === pwmUs)
        .map((p): CompareSeries | null => {
          const days = p.underlying.map((u) => localDay(u.t_start)).filter((d) => d >= from && d <= to);
          if (!days.length) return null;
          const day = days.sort().at(-1)!;
          const underlying = p.underlying.filter((u) => localDay(u.t_start) === day);
          const first = Math.min(...underlying.map((u) => u.repeat ?? 1));
          const acoustic = underlying
            .filter((u) => (u.repeat ?? 1) === first)
            .flatMap((u) => u.acoustic)
            .sort((a, b) => b.elevation_deg - a.elevation_deg);
          return {
            id: `${k.slug}::${p.id}@${day}`,
            keySlug: k.slug,
            pointId: p.id,
            pwm_us: p.pwm_us,
            acoustic,
            underlying,
            label: `${labelForKey(k.slug)} · ${p.pwm_us}µs · ${day}`,
            color: '',
          };
        })
        .filter((x): x is CompareSeries => x !== null);
    }),
  );
  return perKey.flat();
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
  // Point ids ("2000-0") repeat across bases, so the list carries the base it was loaded for:
  // an Add while a new base's points are still loading must not pair the new label with the
  // previous base's mics.
  const [loaded, setLoaded] = useState<{ key: string; points: MergedPWMPoint[] }>({ key: '', points: [] });
  const points = loaded.key === selKey ? loaded.points : [];
  const [selPoint, setSelPoint] = useState('');
  const [dayFrom, setDayFrom] = useState(() => new Date().toLocaleDateString('sv'));
  const [dayTo, setDayTo] = useState(() => new Date().toLocaleDateString('sv'));
  const [dayPwm, setDayPwm] = useState(2000);
  const [dayIds, setDayIds] = useState<string[]>([]);
  const [dayBusy, setDayBusy] = useState(false);
  const [dayMsg, setDayMsg] = useState('');

  const toggleDay = async () => {
    if (dayIds.length) {
      dayIds.forEach(onRemove);
      setDayIds([]);
      setDayMsg('');
      return;
    }
    setDayBusy(true);
    try {
      const found = await seriesForDays(keys, dayFrom, dayTo, dayPwm, labelForKey);
      found.forEach(onAdd);
      setDayIds(found.map((f) => f.id));
      const span = dayFrom === dayTo ? `on ${dayTo}` : `from ${dayFrom} to ${dayTo}`;
      setDayMsg(found.length ? '' : `No captures at ${dayPwm} µs ${span}`);
    } finally {
      setDayBusy(false);
    }
  };

  useEffect(() => {
    if (!selKey) return;
    let cancelled = false;
    api.listPWMPoints(selKey).then(
      (p) => { if (!cancelled) { setLoaded({ key: selKey, points: p }); setSelPoint(p[0]?.id ?? ''); } },
      () => !cancelled && setLoaded({ key: selKey, points: [] }),
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
      underlying: p.underlying,
      label: `${labelForKey(selKey)} · ${p.pwm_us}µs`,
      color: '',
    });
  };

  return (
    <div className="bg-gray-800 border border-gray-700 rounded-md p-3 space-y-3">
      <div className="text-xs uppercase tracking-wide text-gray-400">Compare bases (overlay)</div>

      <div className="flex flex-wrap items-end gap-2">
        <label className="block">
          <span className="text-[11px] text-gray-500">
            Base<InfoToggle label="arc orientation marks">{BASE_HELP.arcMark}</InfoToggle>
          </span>
          <select
            className="input mt-1 min-w-[24rem]"
            value={selKey}
            onChange={(e) => setSelKey(e.target.value)}
          >
            <option value="">— pick a base —</option>
            {keys.map((k) => (
              <option key={k.slug} value={k.slug}>
                {keyLabel(k)}
              </option>
            ))}
          </select>
        </label>
        <label className="block">
          <span className="text-[11px] text-gray-500">ESC signal point</span>
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

      <div className="flex flex-wrap items-end gap-2">
        <label className="block">
          <span className="text-[11px] text-gray-500">From</span>
          <input
            type="date"
            className="input mt-1"
            value={dayFrom}
            max={dayTo}
            disabled={dayIds.length > 0}
            onChange={(e) => setDayFrom(e.target.value)}
          />
        </label>
        <label className="block">
          <span className="text-[11px] text-gray-500">To</span>
          <input
            type="date"
            className="input mt-1"
            value={dayTo}
            min={dayFrom}
            disabled={dayIds.length > 0}
            onChange={(e) => setDayTo(e.target.value)}
          />
        </label>
        <label className="block">
          <span className="text-[11px] text-gray-500">ESC signal (µs)</span>
          <input
            type="number"
            className="input mt-1 w-24 font-mono"
            min={1000}
            max={2000}
            step={50}
            value={dayPwm}
            disabled={dayIds.length > 0}
            onChange={(e) => setDayPwm(Number(e.target.value))}
          />
        </label>
        <label className="inline-flex items-center gap-2 text-sm text-gray-200 py-2">
          <input
            type="checkbox"
            checked={dayIds.length > 0}
            disabled={dayBusy || !dayFrom || !dayTo || dayFrom > dayTo}
            onChange={toggleDay}
          />
          Show every base from these days
        </label>
        {dayBusy && <span className="text-xs text-gray-500 py-2">loading…</span>}
        {dayMsg && <span className="text-xs text-amber-400 py-2">{dayMsg}</span>}
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
              <span className="text-[10px] text-gray-500 uppercase px-1">current</span>
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
