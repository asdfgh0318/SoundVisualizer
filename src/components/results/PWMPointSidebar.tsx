import { useState } from 'react';
import type { MergedPWMPoint, UnderlyingCapture } from '../../api/types';

interface Props {
  points: MergedPWMPoint[];
  selectedId: string | null;
  drilldownTStart: string | null;
  onSelect: (id: string) => void;
  onDrilldown: (mergedId: string, t_start: string | null) => void;
}

export function PWMPointSidebar({
  points, selectedId, drilldownTStart, onSelect, onDrilldown,
}: Props) {
  if (points.length === 0) {
    return <div className="text-sm text-gray-400 italic p-3">No PWM points yet.</div>;
  }
  return (
    <ul className="space-y-1">
      {points.map((p) => (
        <PWMRow
          key={p.id}
          point={p}
          selected={p.id === selectedId}
          drilldownTStart={p.id === selectedId ? drilldownTStart : null}
          onSelect={() => onSelect(p.id)}
          onDrilldown={(t) => onDrilldown(p.id, t)}
        />
      ))}
    </ul>
  );
}

function PWMRow({
  point, selected, drilldownTStart, onSelect, onDrilldown,
}: {
  point: MergedPWMPoint;
  selected: boolean;
  drilldownTStart: string | null;
  onSelect: () => void;
  onDrilldown: (t_start: string | null) => void;
}) {
  const [expanded, setExpanded] = useState(false);
  const isMerged = point.underlying.length > 1;
  const onlyOneHalf =
    point.underlying.length === 1 &&
    (point.composition.top === 0 || point.composition.bottom === 0);

  return (
    <li>
      <div
        className={`rounded-md border ${
          selected
            ? 'bg-indigo-600/30 border-indigo-500/60'
            : 'border-gray-700 hover:border-gray-600'
        }`}
      >
        <button
          type="button"
          onClick={() => {
            onSelect();
            if (drilldownTStart !== null) onDrilldown(null);
          }}
          className={`w-full text-left px-3 py-2 text-sm transition-colors ${
            selected ? 'text-white' : 'text-gray-300'
          }`}
        >
          <div className="flex items-center justify-between gap-2">
            <span className="font-semibold text-gray-100">PWM {point.pwm_us} µs</span>
            <CompositionChip composition={point.composition} singleHalf={onlyOneHalf} />
          </div>
          <div className="text-[11px] text-gray-500 mt-0.5">{point.acoustic.length} mics</div>
        </button>

        {isMerged && (
          <div className="border-t border-gray-700/50">
            <button
              type="button"
              onClick={() => setExpanded((v) => !v)}
              className="w-full text-left px-3 py-1.5 text-[11px] text-gray-400 hover:text-gray-200"
            >
              {expanded ? '▾' : '▸'} {point.underlying.length} captures
              {drilldownTStart && (
                <span className="ml-2 text-amber-400 uppercase tracking-wide">drilled in</span>
              )}
            </button>
            {expanded && (
              <ul className="px-3 pb-2 space-y-1">
                {drilldownTStart && (
                  <li>
                    <button
                      type="button"
                      onClick={() => onDrilldown(null)}
                      className="text-[11px] text-indigo-400 hover:text-indigo-300 underline"
                    >
                      ← Back to merged view
                    </button>
                  </li>
                )}
                {point.underlying.map((u) => (
                  <UnderlyingRow
                    key={u.t_start}
                    capture={u}
                    isDrilled={drilldownTStart === u.t_start}
                    onClick={() => {
                      onSelect();
                      onDrilldown(u.t_start);
                    }}
                  />
                ))}
              </ul>
            )}
          </div>
        )}
      </div>
    </li>
  );
}

function UnderlyingRow({
  capture, isDrilled, onClick,
}: {
  capture: UnderlyingCapture;
  isDrilled: boolean;
  onClick: () => void;
}) {
  const time = capture.t_start.slice(11, 19);
  return (
    <li>
      <button
        type="button"
        onClick={onClick}
        className={`w-full text-left px-2 py-1 rounded text-[11px] font-mono flex items-center justify-between gap-2 ${
          isDrilled
            ? 'bg-amber-500/20 text-amber-200 border border-amber-500/50'
            : 'text-gray-300 hover:bg-gray-700/40'
        }`}
      >
        <span>{time}</span>
        <span
          className={`uppercase tracking-wide px-1.5 py-0.5 rounded text-[10px] ${
            capture.half === 'top'
              ? 'bg-sky-500/20 text-sky-300'
              : 'bg-rose-500/20 text-rose-300'
          }`}
        >
          {capture.half}
        </span>
      </button>
    </li>
  );
}

function CompositionChip({
  composition, singleHalf,
}: {
  composition: Record<string, number>;
  singleHalf: boolean;
}) {
  const top = composition.top ?? 0;
  const bot = composition.bottom ?? 0;

  if (singleHalf) {
    // A single capture from one half — flag explicitly so the user notices that
    // the other half is missing (or was split off as incompatible).
    const label = top > 0 ? 'TOP only' : 'BOT only';
    return (
      <span className="text-[10px] uppercase tracking-wide px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/40">
        {label}
      </span>
    );
  }

  // Standard merged case
  if (top === 1 && bot === 1) {
    return (
      <span className="text-[10px] uppercase tracking-wide px-1.5 py-0.5 rounded bg-indigo-500/20 text-indigo-300">
        T+B
      </span>
    );
  }

  // Non-standard composition — show explicit counts
  const parts: string[] = [];
  if (top > 0) parts.push(`${top}T`);
  if (bot > 0) parts.push(`${bot}B`);
  return (
    <span className="text-[10px] uppercase tracking-wide px-1.5 py-0.5 rounded bg-indigo-500/20 text-indigo-300">
      {parts.join(' + ')}
    </span>
  );
}
