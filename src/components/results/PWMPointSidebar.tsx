import type { PWMPoint } from '../../api/types';

interface Props {
  points: PWMPoint[];
  selectedT: string | null;
  onSelect: (t: string) => void;
}

export function PWMPointSidebar({ points, selectedT, onSelect }: Props) {
  if (points.length === 0) {
    return <div className="text-sm text-gray-400 italic p-3">No PWM points yet.</div>;
  }

  return (
    <ul className="space-y-1">
      {points.map((p) => {
        const active = p.t_start === selectedT;
        return (
          <li key={p.t_start}>
            <button
              type="button"
              onClick={() => onSelect(p.t_start)}
              className={`w-full text-left px-3 py-2 rounded-md text-sm transition-colors ${
                active
                  ? 'bg-indigo-600/30 border border-indigo-500/60 text-white'
                  : 'border border-gray-700 hover:border-gray-600 text-gray-300'
              }`}
            >
              <div className="font-mono text-xs text-gray-400">
                {p.t_start.slice(0, 19).replace('T', ' ')}
              </div>
              <div className="flex items-center justify-between mt-0.5">
                <span className="font-semibold text-gray-100">
                  PWM {p.pwm_us ?? '—'} µs
                </span>
                <span
                  className={`text-[10px] uppercase tracking-wide px-1.5 py-0.5 rounded ${
                    p.half === 'top'
                      ? 'bg-sky-500/20 text-sky-300'
                      : p.half === 'bottom'
                        ? 'bg-rose-500/20 text-rose-300'
                        : 'bg-gray-500/20 text-gray-400'
                  }`}
                >
                  {p.half ?? '—'}
                </span>
              </div>
              <div className="text-[11px] text-gray-500 mt-0.5">
                {p.acoustic.length} mics
              </div>
            </button>
          </li>
        );
      })}
    </ul>
  );
}
