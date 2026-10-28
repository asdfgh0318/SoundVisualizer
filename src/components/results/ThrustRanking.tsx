import type { CompareSeries } from './compareSeries';

const RANK_PWM_US = 2000;

interface Row {
  id: string;
  label: string;
  color: string;
  mean: number;
  min: number;
  max: number;
  n: number;
}

function rows(series: CompareSeries[]): Row[] {
  return series
    .filter((s) => s.pwm_us === RANK_PWM_US)
    .map((s) => {
      const t = s.underlying
        .map((u) => u.performance_summary?.thrust_n_mean)
        .filter((v): v is number => typeof v === 'number' && Number.isFinite(v));
      if (!t.length) return null;
      return {
        id: s.id,
        label: s.label.replace(` · ${RANK_PWM_US}µs`, ''),
        color: s.color,
        mean: t.reduce((a, b) => a + b, 0) / t.length,
        min: Math.min(...t),
        max: Math.max(...t),
        n: t.length,
      };
    })
    .filter((r): r is Row => r !== null)
    .sort((a, b) => Math.abs(b.mean) - Math.abs(a.mean));
}

/** Overlaid series at 2000 µs ranked by thrust magnitude, each the mean over its repeats. */
export function ThrustRanking({ series }: { series: CompareSeries[] }) {
  const ranked = rows(series);
  if (!ranked.length) return null;
  return (
    <div className="bg-gray-800 border border-gray-700 rounded-md p-3 space-y-2">
      <div className="text-xs uppercase tracking-wide text-gray-400">
        Thrust at {RANK_PWM_US} µs
      </div>
      <div className="text-[11px] text-gray-500">
        Overlaid bases, largest first; mean over repeats (range in brackets).
      </div>
      <ol className="space-y-1.5">
        {ranked.map((r, i) => (
          <li key={r.id} className="flex items-start gap-2 text-xs">
            <span className="text-gray-500 font-mono w-4 shrink-0 text-right">{i + 1}</span>
            <span className="inline-block w-2.5 h-2.5 rounded-full mt-1 shrink-0" style={{ background: r.color }} />
            <span className="flex-1 min-w-0 text-gray-300 break-words">{r.label}</span>
            <span className="text-right shrink-0">
              <span className="font-mono text-gray-100">{r.mean.toFixed(2)} N</span>
              <span className="block font-mono text-[10px] text-gray-500">
                n={r.n}{r.n > 1 ? ` [${r.min.toFixed(2)}…${r.max.toFixed(2)}]` : ''}
              </span>
            </span>
          </li>
        ))}
      </ol>
    </div>
  );
}
