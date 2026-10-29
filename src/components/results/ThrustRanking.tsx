import { useState } from 'react';
import type { CompareSeries } from './compareSeries';
import type { ArcLevels } from './PolarTab';

const RANK_PWM_US = 2000;
// The stand's rpm channel is electrical; AXI 2217/12 has 14 poles (verified against the audio BPF, 2026-10-27).
const MECH_PER_ELEC = 60 / 7;

type SortBy = 'thrust' | 'quiet' | 'rpm';

const SORTS: { key: SortBy; label: string }[] = [
  { key: 'thrust', label: 'Most thrust' },
  { key: 'quiet', label: 'Quietest' },
  { key: 'rpm', label: 'Most rpm' },
];

interface Stat {
  mean: number;
  min: number;
  max: number;
}

interface Row {
  id: string;
  label: string;
  color: string;
  thrust: Stat;
  n: number;
  rpm: Stat | null;
  level: number | null;
}

function stat(v: number[]): Stat | null {
  if (!v.length) return null;
  return { mean: v.reduce((a, b) => a + b, 0) / v.length, min: Math.min(...v), max: Math.max(...v) };
}

const finite = (v: number | undefined): v is number => typeof v === 'number' && Number.isFinite(v);

// Rows missing the sort quantity go last rather than being dropped.
const last = (v: number | null | undefined, sign: 1 | -1) => (v == null ? Infinity : sign * v);

function rows(series: CompareSeries[], arcLevels: ArcLevels | null, sortBy: SortBy): Row[] {
  const out = series
    .filter((s) => s.pwm_us === RANK_PWM_US)
    .map((s): Row | null => {
      const thrust = stat(s.underlying.map((u) => u.performance_summary?.thrust_n_mean).filter(finite));
      if (!thrust) return null;
      const rpm = s.underlying
        .map((u) => u.performance_summary?.rpm_mean)
        .filter(finite)
        .filter((v) => v > 0)
        .map((v) => v * MECH_PER_ELEC);
      return {
        id: s.id,
        label: s.label.replace(` · ${RANK_PWM_US}µs`, ''),
        color: s.color,
        thrust,
        n: s.underlying.filter((u) => finite(u.performance_summary?.thrust_n_mean)).length,
        rpm: stat(rpm),
        level: arcLevels?.bySeries[s.id] ?? null,
      };
    })
    .filter((r): r is Row => r !== null);
  const key: Record<SortBy, (r: Row) => number> = {
    thrust: (r) => -Math.abs(r.thrust.mean),
    quiet: (r) => last(r.level, 1),
    rpm: (r) => last(r.rpm?.mean, -1),
  };
  return out.sort((a, b) => key[sortBy](a) - key[sortBy](b));
}

const range = (s: Stat, digits: number) =>
  `[${s.min.toLocaleString('en', { maximumFractionDigits: digits, minimumFractionDigits: digits })}…${s.max.toLocaleString('en', { maximumFractionDigits: digits, minimumFractionDigits: digits })}]`;

/** Overlaid series at 2000 µs with thrust, rpm and (on the Polar tab) arc level, sortable. */
export function ThrustRanking({ series, arcLevels }: { series: CompareSeries[]; arcLevels: ArcLevels | null }) {
  const [chosen, setSortBy] = useState<SortBy>('thrust');
  const sortBy: SortBy = chosen === 'quiet' && !arcLevels ? 'thrust' : chosen;
  const ranked = rows(series, arcLevels, sortBy);
  if (!ranked.length) return null;
  return (
    <div className="bg-gray-800 border border-gray-700 rounded-md p-3 space-y-2">
      <div className="text-xs uppercase tracking-wide text-gray-400">At {RANK_PWM_US} µs</div>
      <div className="flex gap-1">
        {SORTS.map((o) => (
          <button
            key={o.key}
            type="button"
            onClick={() => setSortBy(o.key)}
            disabled={o.key === 'quiet' && !arcLevels}
            title={o.key === 'quiet' && !arcLevels ? 'Open the Polar tab to rank by level' : undefined}
            className={`text-[11px] rounded px-2 py-1 border disabled:opacity-40 disabled:cursor-not-allowed ${
              sortBy === o.key
                ? 'bg-indigo-600/40 border-indigo-500/60 text-white'
                : 'border-gray-600 text-gray-300 hover:border-indigo-500'
            }`}
          >
            {o.label}
          </button>
        ))}
      </div>
      <div className="text-[11px] text-gray-500">
        Mean over repeats, range in brackets. rpm is the stand's electrical reading × 60/7 (AXI 2217/12, 14 poles).
        {arcLevels
          ? <> Level: energy mean over the mics of each mic's repeat-mean, {arcLevels.what}, {arcLevels.unit}.</>
          : <> Level appears on the Polar tab.</>}
      </div>
      <ol className="space-y-2">
        {ranked.map((r, i) => (
          <li key={r.id} className="flex items-start gap-2 text-xs">
            <span className="text-gray-500 font-mono w-4 shrink-0 text-right">{i + 1}</span>
            <span className="inline-block w-2.5 h-2.5 rounded-full mt-1 shrink-0" style={{ background: r.color }} />
            <span className="flex-1 min-w-0 text-gray-300 break-words">{r.label}</span>
            <span className="text-right shrink-0 font-mono">
              <span className={`block ${sortBy === 'thrust' ? 'text-white' : 'text-gray-300'}`}>{r.thrust.mean.toFixed(2)} N</span>
              {r.n > 1 && <span className="block text-[10px] text-gray-500">{range(r.thrust, 2)}</span>}
              {r.rpm && (
                <>
                  <span className={`block ${sortBy === 'rpm' ? 'text-white' : 'text-gray-300'}`}>
                    {Math.round(r.rpm.mean).toLocaleString('en')} rpm
                  </span>
                  {r.n > 1 && <span className="block text-[10px] text-gray-500">{range(r.rpm, 0)}</span>}
                </>
              )}
              {r.level != null && (
                <span className={`block ${sortBy === 'quiet' ? 'text-white' : 'text-gray-300'}`}>
                  {r.level.toFixed(1)} {arcLevels?.unit === 'dB SPL' ? 'dB' : 'dBFS'}
                </span>
              )}
            </span>
          </li>
        ))}
      </ol>
    </div>
  );
}
