import { useMemo } from 'react';
import type { SplResult } from '../../types/index.ts';
import { ELEVATION_ANGLES } from '../../types/index.ts';
import { formatAzimuth, formatElevation } from '../../utils/angles.ts';

interface PolarPlotProps {
  data: SplResult[];
  size?: number;
}

const SPOKE_COUNT = 24; // every 15 degrees

/**
 * Maps elevation (-90..+90) to radius (center = +90 top, outer = -90 bottom).
 * This puts the "top" mic at center, "bottom" mic at edge.
 */
function elevationToRadius(elevDeg: number, maxRadius: number): number {
  // -90 -> maxRadius, +90 -> 0
  return ((90 - elevDeg) / 180) * maxRadius;
}

function splToColor(splDb: number, minSpl: number, maxSpl: number): string {
  if (!isFinite(splDb)) return '#333';
  const range = maxSpl - minSpl;
  const t = range > 0 ? (splDb - minSpl) / range : 0.5;
  // Blue (cold/quiet) -> Yellow -> Red (hot/loud)
  const r = Math.round(255 * Math.min(1, t * 2));
  const g = Math.round(255 * Math.min(1, (1 - Math.abs(t - 0.5) * 2)));
  const b = Math.round(255 * Math.max(0, 1 - t * 2));
  return `rgb(${r},${g},${b})`;
}

export function PolarPlot({ data, size = 400 }: PolarPlotProps) {
  const center = size / 2;
  const maxRadius = size * 0.42;
  const padding = size * 0.08;

  const { minSpl, maxSpl } = useMemo(() => {
    const finite = data.filter((d) => isFinite(d.splDb));
    if (finite.length === 0) return { minSpl: -60, maxSpl: 0 };
    const vals = finite.map((d) => d.splDb);
    return { minSpl: Math.min(...vals), maxSpl: Math.max(...vals) };
  }, [data]);

  return (
    <svg
      viewBox={`0 0 ${size} ${size}`}
      width={size}
      height={size}
      className="mx-auto"
      aria-label="Polar sound distribution plot"
    >
      {/* Background */}
      <rect width={size} height={size} fill="#111827" rx="8" />

      {/* Grid rings (elevation) */}
      {ELEVATION_ANGLES.map((elev) => {
        const r = elevationToRadius(elev, maxRadius);
        return (
          <g key={`ring-${elev}`}>
            <circle
              cx={center}
              cy={center}
              r={r}
              fill="none"
              stroke="#374151"
              strokeWidth="0.5"
            />
            <text
              x={center + r + 3}
              y={center - 3}
              fill="#6b7280"
              fontSize="9"
            >
              {formatElevation(elev)}
            </text>
          </g>
        );
      })}

      {/* Radial spokes (azimuth) */}
      {Array.from({ length: SPOKE_COUNT }, (_, i) => {
        const angleDeg = i * (360 / SPOKE_COUNT);
        const angleRad = ((angleDeg - 90) * Math.PI) / 180; // -90 so 0° is up
        const x2 = center + maxRadius * Math.cos(angleRad);
        const y2 = center + maxRadius * Math.sin(angleRad);
        const labelX = center + (maxRadius + padding * 0.6) * Math.cos(angleRad);
        const labelY = center + (maxRadius + padding * 0.6) * Math.sin(angleRad);
        return (
          <g key={`spoke-${angleDeg}`}>
            <line
              x1={center}
              y1={center}
              x2={x2}
              y2={y2}
              stroke="#374151"
              strokeWidth="0.5"
            />
            {angleDeg % 30 === 0 && (
              <text
                x={labelX}
                y={labelY}
                fill="#9ca3af"
                fontSize="9"
                textAnchor="middle"
                dominantBaseline="central"
              >
                {formatAzimuth(angleDeg)}
              </text>
            )}
          </g>
        );
      })}

      {/* Data points */}
      {data.map((d, i) => {
        if (!isFinite(d.splDb)) return null;
        const r = elevationToRadius(d.elevationDeg, maxRadius);
        const angleRad = ((d.azimuthDeg - 90) * Math.PI) / 180;
        const x = center + r * Math.cos(angleRad);
        const y = center + r * Math.sin(angleRad);
        const color = splToColor(d.splDb, minSpl, maxSpl);
        return (
          <circle
            key={i}
            cx={x}
            cy={y}
            r={5}
            fill={color}
            stroke="#fff"
            strokeWidth="0.5"
            opacity={0.85}
          >
            <title>
              Az: {formatAzimuth(d.azimuthDeg)}, El: {formatElevation(d.elevationDeg)},{' '}
              {d.splDb.toFixed(1)} dB
            </title>
          </circle>
        );
      })}

      {/* Empty state */}
      {data.length === 0 && (
        <text
          x={center}
          y={center}
          fill="#6b7280"
          fontSize="12"
          textAnchor="middle"
          dominantBaseline="central"
        >
          No data — capture measurements first
        </text>
      )}

      {/* Color scale legend */}
      {data.length > 0 && (
        <g transform={`translate(${size - 30}, ${size * 0.2})`}>
          <defs>
            <linearGradient id="spl-gradient" x1="0" y1="1" x2="0" y2="0">
              <stop offset="0%" stopColor="rgb(0,0,255)" />
              <stop offset="50%" stopColor="rgb(255,255,0)" />
              <stop offset="100%" stopColor="rgb(255,0,0)" />
            </linearGradient>
          </defs>
          <rect width="12" height={size * 0.6} fill="url(#spl-gradient)" rx="2" />
          <text x="16" y="0" fill="#9ca3af" fontSize="8" dominantBaseline="hanging">
            {maxSpl.toFixed(0)} dB
          </text>
          <text x="16" y={size * 0.6} fill="#9ca3af" fontSize="8">
            {minSpl.toFixed(0)} dB
          </text>
        </g>
      )}
    </svg>
  );
}
