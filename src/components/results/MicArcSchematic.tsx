import { useMemo } from 'react';
import { useSetupStore } from '../../stores/setupStore';

interface Props {
  /** Serials drawn in the plot next to this schematic; the others are dimmed. */
  activeSerials?: string[];
}

const W = 170;
const H = 200;
const CX = 34;
const CY = H / 2;
const R = 78;

/** Side view of the microphone arc as configured on the Setup page: +90° at the
 *  top, 0° in the propeller plane to the right, −90° below. Elevation only —
 *  the rig has no azimuth axis. */
export function MicArcSchematic({ activeSerials }: Props) {
  const mics = useSetupStore((s) => s.mics);
  const placed = useMemo(
    () =>
      mics
        .filter((m) => m.elevationDeg !== null)
        .map((m) => ({ ...m, elevationDeg: m.elevationDeg as number }))
        .sort((a, b) => b.elevationDeg - a.elevationDeg),
    [mics],
  );
  const unplaced = mics.filter((m) => m.elevationDeg === null);
  const active = activeSerials ? new Set(activeSerials) : null;

  const pos = (e: number) => {
    const rad = (e * Math.PI) / 180;
    return { x: CX + R * Math.cos(rad), y: CY - R * Math.sin(rad) };
  };
  const top = pos(90);
  const bottom = pos(-90);

  return (
    <div className="text-xs text-gray-400">
      <div className="uppercase tracking-wide text-[11px] text-gray-500 mb-1">Mic arc (side view)</div>
      <svg
        viewBox={`0 0 ${W} ${H}`}
        width="100%"
        role="img"
        aria-label={`Microphone arc: ${placed.map((m) => `${m.serial || 'mic'} at ${m.elevationDeg}°`).join(', ') || 'no microphones placed'}`}
        className="max-w-[11rem]"
      >
        {/* arc */}
        <path
          d={`M ${top.x} ${top.y} A ${R} ${R} 0 0 1 ${bottom.x} ${bottom.y}`}
          fill="none"
          stroke="#4b5563"
          strokeWidth="1.5"
        />
        {/* propeller plane and axis */}
        <line x1={CX} y1={CY} x2={CX + R + 6} y2={CY} stroke="#374151" strokeDasharray="3 3" />
        <line x1={CX} y1={CY - R - 6} x2={CX} y2={CY + R + 6} stroke="#374151" strokeDasharray="3 3" />
        {/* propeller at the hub */}
        <line x1={CX - 14} y1={CY} x2={CX + 14} y2={CY} stroke="#9ca3af" strokeWidth="3" strokeLinecap="round" />
        <circle cx={CX} cy={CY} r="3.5" fill="#d1d5db" />
        {/* angle labels */}
        <text x={CX + 4} y={CY - R - 9} fill="#6b7280" fontSize="9">+90°</text>
        <text x={CX + R + 8} y={CY + 3} fill="#6b7280" fontSize="9">0°</text>
        <text x={CX + 4} y={CY + R + 16} fill="#6b7280" fontSize="9">−90°</text>
        {/* microphones */}
        {placed.map((m) => {
          const p = pos(m.elevationDeg);
          const dim = active !== null && !active.has(m.serial);
          const label = m.serial || `#${mics.indexOf(m) + 1}`;
          return (
            <g key={m.id} opacity={dim ? 0.3 : 1}>
              <title>{`${label} · ${m.elevationDeg}°`}</title>
              <circle cx={p.x} cy={p.y} r="4" fill="#6366f1" stroke="#c7d2fe" strokeWidth="1" />
              <text
                x={p.x + 7}
                y={p.y + 3}
                fill="#d1d5db"
                fontSize="8"
                fontFamily="ui-monospace, monospace"
              >
                {label}
              </text>
            </g>
          );
        })}
      </svg>
      {placed.length === 0 && (
        <p className="text-[11px] text-gray-500 mt-1">
          No microphone has an elevation yet. Set them on the Setup page.
        </p>
      )}
      {unplaced.length > 0 && (
        <p className="text-[11px] text-gray-500 mt-1">
          Unplaced: {unplaced.map((m) => m.serial || 'no serial').join(', ')}
        </p>
      )}
    </div>
  );
}
