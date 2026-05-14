import { useEffect, useState } from 'react';
import { api, ApiError } from '../../api/client';
import type { AcousticInPoint, MergedPWMPoint, PsychoacousticMetrics } from '../../api/types';

interface Props {
  keySlug: string;
  point: MergedPWMPoint;
}

interface Row {
  mic: AcousticInPoint;
  metrics: PsychoacousticMetrics | null;
  error: string | null;
}

export function PsychoacousticsTab({ keySlug, point }: Props) {
  const [rows, setRows] = useState<Row[]>(() =>
    point.acoustic.map((m) => ({ mic: m, metrics: null, error: null })),
  );

  useEffect(() => {
    setRows(point.acoustic.map((m) => ({ mic: m, metrics: null, error: null })));
    let cancelled = false;

    // Fetch per-mic metrics in parallel. Server caches after first compute.
    point.acoustic.forEach((mic) => {
      api.getPsychoacoustics(keySlug, mic.id).then(
        (m) => {
          if (cancelled) return;
          setRows((prev) =>
            prev.map((r) => (r.mic.id === mic.id ? { ...r, metrics: m } : r)),
          );
        },
        (e: Error | ApiError) => {
          if (cancelled) return;
          setRows((prev) =>
            prev.map((r) => (r.mic.id === mic.id ? { ...r, error: e.message } : r)),
          );
        },
      );
    });

    return () => { cancelled = true; };
  }, [keySlug, point.acoustic]);

  const someAssumedZeroF =
    rows.some((r) => r.metrics?.fluctuation_assumed_zero);

  const ranges = computeRanges(rows);

  return (
    <div className="space-y-4">
      <div className="bg-gray-800 border border-gray-700 rounded-md p-4">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-gray-200 mb-1">
          Sound quality metrics + Psychoacoustic Annoyance
        </h2>
        <p className="text-xs text-gray-400">
          Per mic, computed via <code className="font-mono text-gray-200">mosqito</code> (ISO 532-1
          loudness, DIN 45692 sharpness, Daniel-Weber roughness). PA via Zwicker formula.
          {' '}First request crunches the WAV; subsequent loads are cached.
        </p>
      </div>

      <div className="bg-gray-800 border border-gray-700 rounded-md overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-900/40">
            <tr className="text-left text-gray-400 border-b border-gray-700">
              <th className="py-2 px-3 font-medium">Elev.</th>
              <th className="py-2 px-3 font-medium">Mic</th>
              <th className="py-2 px-3 font-medium text-right">Loudness <span className="text-gray-500">sone</span></th>
              <th className="py-2 px-3 font-medium text-right">Sharpness <span className="text-gray-500">acum</span></th>
              <th className="py-2 px-3 font-medium text-right">Roughness <span className="text-gray-500">asper</span></th>
              <th className="py-2 px-3 font-medium text-right">Fluctuation <span className="text-gray-500">vacil</span></th>
              <th className="py-2 px-3 font-medium text-right">PA</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.mic.id} className="border-b border-gray-700/50 last:border-b-0">
                <td className="py-2 px-3 font-mono text-gray-200">
                  {r.mic.elevation_deg > 0 ? '+' : ''}
                  {r.mic.elevation_deg}°
                </td>
                <td className="py-2 px-3 text-xs text-gray-400 font-mono">{r.mic.mic_serial}</td>
                {r.error && (
                  <td colSpan={5} className="py-2 px-3 text-red-400 text-xs">
                    error: {r.error}
                  </td>
                )}
                {!r.error && !r.metrics && (
                  <td colSpan={5} className="py-2 px-3 text-gray-500 italic text-xs">
                    computing…
                  </td>
                )}
                {!r.error && r.metrics && (
                  <>
                    <Cell
                      value={r.metrics.loudness_sone.toFixed(2)}
                      color={gradientColor(r.metrics.loudness_sone, ranges.loudness)}
                    />
                    <Cell
                      value={r.metrics.sharpness_acum.toFixed(2)}
                      color={gradientColor(r.metrics.sharpness_acum, ranges.sharpness)}
                    />
                    <Cell
                      value={r.metrics.roughness_asper.toFixed(3)}
                      color={gradientColor(r.metrics.roughness_asper, ranges.roughness)}
                    />
                    <Cell
                      value={r.metrics.fluctuation_vacil.toFixed(3)}
                      dim={r.metrics.fluctuation_assumed_zero}
                    />
                    <Cell
                      value={r.metrics.annoyance.toFixed(2)}
                      color={gradientColor(r.metrics.annoyance, ranges.annoyance)}
                      bold
                    />
                  </>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {someAssumedZeroF && (
        <div className="p-3 rounded-md border border-amber-700/60 bg-amber-900/20 text-amber-300 text-xs">
          ⓘ <strong>Fluctuation strength is reported as 0 vacil</strong> — `mosqito` doesn't ship a
          fluctuation-strength implementation yet. Per the report, drone hover F is typically
          ~0.01 vacil (noise floor) and contributes &lt;0.1% to PA, so this is an acceptable
          approximation. Will be revisited once the NOR-145 lands with a hardware reference.
        </div>
      )}

      <div className="text-xs text-gray-500 flex items-center gap-2 flex-wrap">
        <span>
          Loudness / sharpness / roughness are derived from float32 audio in [-1, 1] — relative
          comparisons within a key are valid; absolute sone values assume calibrated dB SPL input,
          which only applies once a UMIK-2 calibration file is uploaded for each mic.
        </span>
        <span className="inline-flex items-center gap-2 ml-auto whitespace-nowrap">
          <span>color scale per column:</span>
          <span className="font-mono" style={{ color: 'hsl(140, 70%, 60%)' }}>best</span>
          <span
            className="h-2 w-24 rounded"
            style={{
              background:
                'linear-gradient(to right, hsl(140,70%,45%), hsl(60,75%,50%), hsl(0,75%,55%))',
            }}
          />
          <span className="font-mono" style={{ color: 'hsl(0, 75%, 62%)' }}>worst</span>
        </span>
      </div>
    </div>
  );
}

interface Range {
  min: number;
  max: number;
}

interface Ranges {
  loudness: Range;
  sharpness: Range;
  roughness: Range;
  annoyance: Range;
}

function computeRanges(rows: Row[]): Ranges {
  const loaded = rows.map((r) => r.metrics).filter((m): m is PsychoacousticMetrics => !!m);
  const pick = (sel: (m: PsychoacousticMetrics) => number): Range => {
    if (loaded.length === 0) return { min: 0, max: 0 };
    const vs = loaded.map(sel);
    return { min: Math.min(...vs), max: Math.max(...vs) };
  };
  return {
    loudness: pick((m) => m.loudness_sone),
    sharpness: pick((m) => m.sharpness_acum),
    roughness: pick((m) => m.roughness_asper),
    annoyance: pick((m) => m.annoyance),
  };
}

// Lower value = better = green. Higher = worse = red. Returns null when the
// column is flat (single row, or all rows tied) so the cell falls back to neutral.
function gradientColor(value: number, range: Range): string | null {
  if (range.max === range.min) return null;
  const t = (value - range.min) / (range.max - range.min); // 0 = best, 1 = worst
  const hue = 140 * (1 - t); // 140 (green) → 0 (red), passing through ~70 (yellow)
  return `hsl(${hue.toFixed(0)}, 75%, 62%)`;
}

function Cell({
  value,
  dim = false,
  color = null,
  bold = false,
}: {
  value: string;
  dim?: boolean;
  color?: string | null;
  bold?: boolean;
}) {
  const fallback = dim ? 'text-gray-500' : 'text-gray-200';
  return (
    <td
      className={`py-2 px-3 font-mono text-right ${color ? '' : fallback} ${bold ? 'font-semibold' : ''}`}
      style={color ? { color } : undefined}
    >
      {value}
    </td>
  );
}
