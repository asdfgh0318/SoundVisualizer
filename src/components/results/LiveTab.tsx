import { useEffect, useMemo, useRef, useState } from 'react';
import { WS_BASE } from '../../api/base';
import { useSetupStore } from '../../stores/setupStore';
import { PolarPolarPlot, type PolarSeries } from './PolarPlot';
import { RangeModeToggle } from './PolarTab';

interface LiveLevel {
  serial: string;
  elevation_deg: number;
  level_db: number | null;
  absolute: boolean;
}

/** Live broadband readout from every configured mic, drawn on the polar.
 *
 *  Built for one job: put a uniform source at the rig and check the arc reads
 *  evenly. A uniform source should draw a circle, so what matters is not the
 *  shape but the SPREAD — max-min across mics, and which mic sits furthest from
 *  the others. Those are surfaced as numbers; the polar is there to show you
 *  *where* on the arc a deviation sits. */
export function LiveTab() {
  const mics = useSetupStore((s) => s.mics);
  const [running, setRunning] = useState(false);
  const [levels, setLevels] = useState<LiveLevel[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [rangeMode, setRangeMode] = useState<180 | 360>(180);
  const [tolerance, setTolerance] = useState(3);
  const [avgSec, setAvgSec] = useState(3);
  const wsRef = useRef<WebSocket | null>(null);
  // Exponential moving average, held in LINEAR POWER per mic. Averaging dB
  // directly under-weights the loud moments and biases every mic low by an
  // amount that depends on how much it fluctuates — which is exactly the
  // between-mic difference this tab exists to measure.
  const emaRef = useRef<Map<string, number>>(new Map());
  const lastTsRef = useRef<number | null>(null);
  const startedRef = useRef<number | null>(null);
  const [settled, setSettled] = useState(false);

  const usable = useMemo(
    () => mics.filter((m) => m.deviceIndex !== null && m.elevationDeg !== null),
    [mics],
  );

  useEffect(() => {
    if (!running) return;
    const ws = new WebSocket(`${WS_BASE}/devices/audio/levels`);
    wsRef.current = ws;
    setError(null);
    emaRef.current = new Map();
    lastTsRef.current = null;
    startedRef.current = Date.now();
    setSettled(false);

    ws.onopen = () =>
      ws.send(
        JSON.stringify({
          mics: usable.map((m) => ({
            serial: m.serial,
            device_index: m.deviceIndex,
            elevation_deg: m.elevationDeg,
            calibration_file_id: m.calibrationFileId,
          })),
        }),
      );
    ws.onmessage = (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.error) {
        setError(msg.error);
        setRunning(false);
        return;
      }
      if (!msg.levels) return;

      const now = Date.now();
      const dt = lastTsRef.current === null ? 0.1 : (now - lastTsRef.current) / 1000;
      lastTsRef.current = now;
      // Time-constant EMA driven by the real frame interval, so the smoothing
      // means the same thing whether frames arrive at 10 Hz or stutter.
      const tau = Math.max(0.1, avgSec);
      const alpha = 1 - Math.exp(-dt / tau);

      const smoothed: LiveLevel[] = (msg.levels as LiveLevel[]).map((l) => {
        if (l.level_db === null || !Number.isFinite(l.level_db)) return l;
        const power = Math.pow(10, l.level_db / 10);
        const prev = emaRef.current.get(l.serial);
        const next = prev === undefined ? power : prev + alpha * (power - prev);
        emaRef.current.set(l.serial, next);
        return { ...l, level_db: 10 * Math.log10(next) };
      });
      setLevels(smoothed);
      if (startedRef.current !== null && now - startedRef.current > tau * 3000) setSettled(true);
    };
    ws.onerror = () => setError('connection failed');
    ws.onclose = (ev) => {
      if (ev.code === 1011) setError(ev.reason || 'refused');
      setRunning(false);
    };

    return () => {
      ws.close();
      wsRef.current = null;
    };
  }, [running, usable, avgSec]);

  const valid = levels.filter((l) => l.level_db !== null && Number.isFinite(l.level_db));
  const allAbsolute = valid.length > 0 && valid.every((l) => l.absolute);
  const unit = allAbsolute ? 'dB SPL' : 'dBFS';

  // Evenness: median is the reference (one bad mic must not drag the target).
  const stats = useMemo(() => {
    if (valid.length < 2) return null;
    const vals = valid.map((l) => l.level_db as number).sort((a, b) => a - b);
    const mid = Math.floor(vals.length / 2);
    const median = vals.length % 2 ? vals[mid] : (vals[mid - 1] + vals[mid]) / 2;
    const spread = vals[vals.length - 1] - vals[0];
    const devs = valid
      .map((l) => ({ ...l, dev: (l.level_db as number) - median }))
      .sort((a, b) => Math.abs(b.dev) - Math.abs(a.dev));
    return { median, spread, devs, outliers: devs.filter((d) => Math.abs(d.dev) > tolerance) };
  }, [valid, tolerance]);

  const series = useMemo<PolarSeries[]>(() => {
    if (valid.length === 0) return [];
    return [
      {
        label: 'live',
        color: '#818cf8',
        points: valid
          .map((l) => ({
            elevation_deg: l.elevation_deg,
            spl_db: l.level_db as number,
            mic_serial: l.serial,
          }))
          .sort((a, b) => b.elevation_deg - a.elevation_deg),
      },
    ];
  }, [valid]);

  return (
    <div className="space-y-4">
      <div className="bg-gray-800 border border-gray-700 rounded-md p-3 space-y-3">
        <p className="text-xs text-gray-400">
          Live broadband level from every configured mic. Put a uniform source at the rig — an
          even arc draws a circle, so read the <strong className="text-gray-200">spread</strong>,
          not the shape. Cannot run during a capture: a device can&apos;t be opened twice.
        </p>

        <div className="flex flex-wrap items-center gap-3">
          <button
            type="button"
            onClick={() => setRunning((r) => !r)}
            disabled={usable.length === 0}
            className={`px-3 py-1.5 rounded-md text-sm font-medium ${
              running
                ? 'bg-red-600 hover:bg-red-500 text-white'
                : 'bg-indigo-600 hover:bg-indigo-500 text-white disabled:opacity-40'
            }`}
          >
            {running ? 'Stop' : 'Start live readout'}
          </button>

          <span className="text-xs text-gray-500">
            {usable.length} mic{usable.length === 1 ? '' : 's'} configured
            {usable.length < mics.length && (
              <span className="text-amber-400"> · {mics.length - usable.length} unusable</span>
            )}
          </span>

          <label className="text-xs text-gray-400 flex items-center gap-2 ml-auto">
            Averaging
            <select
              value={avgSec}
              onChange={(e) => setAvgSec(Number(e.target.value))}
              className="input py-1"
            >
              <option value={0.5}>0.5 s (fast)</option>
              <option value={3}>3 s</option>
              <option value={10}>10 s</option>
              <option value={30}>30 s (steady)</option>
            </select>
          </label>

          <label className="text-xs text-gray-400 flex items-center gap-2">
            Tolerance ±
            <input
              type="number"
              value={tolerance}
              min={0.5}
              step={0.5}
              onChange={(e) => setTolerance(Number(e.target.value))}
              className="input w-16 py-1"
            />
            dB
          </label>
          <RangeModeToggle value={rangeMode} onChange={setRangeMode} />
        </div>

        {usable.length === 0 && (
          <p className="text-xs text-amber-400">
            No mics with both a device and an elevation. Set them up in <strong>Setup</strong> first.
          </p>
        )}
        {running && !settled && (
          <p className="text-xs text-amber-400">
            Settling — the average needs about {(avgSec * 3).toFixed(0)} s before the spread is
            trustworthy.
          </p>
        )}
        {error && <p className="text-xs text-red-400">⚠ {error}</p>}
      </div>

      {stats && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-px bg-gray-700 border border-gray-700 rounded-md overflow-hidden">
          <Stat label="Spread (max−min)" value={`${stats.spread.toFixed(1)} dB`}
                tone={stats.spread > tolerance * 2 ? 'bad' : 'ok'} />
          <Stat label="Median" value={`${stats.median.toFixed(1)} ${unit}`} tone="neutral" />
          <Stat label="Outliers" value={`${stats.outliers.length} / ${valid.length}`}
                tone={stats.outliers.length ? 'bad' : 'ok'} />
          <Stat label="Worst mic"
                value={stats.devs[0] ? `${stats.devs[0].serial} ${stats.devs[0].dev >= 0 ? '+' : ''}${stats.devs[0].dev.toFixed(1)}` : '—'}
                tone={stats.devs[0] && Math.abs(stats.devs[0].dev) > tolerance ? 'bad' : 'ok'} />
        </div>
      )}

      <div className="bg-gray-800 border border-gray-700 rounded-md p-3">
        {series.length > 0 ? (
          <PolarPolarPlot series={series} rangeMode={rangeMode} unit={unit} />
        ) : (
          <p className="text-sm text-gray-500 py-8 text-center">
            {running ? 'waiting for the first frame…' : 'Not running.'}
          </p>
        )}
      </div>

      {stats && (
        <div className="overflow-x-auto border border-gray-700 rounded-md">
          <table className="w-full text-sm min-w-[24rem]">
            <thead>
              <tr className="bg-gray-800 text-gray-400 text-xs uppercase tracking-wide">
                <th className="text-left px-3 py-2">Mic</th>
                <th className="text-right px-3 py-2">Elev</th>
                <th className="text-right px-3 py-2">Level</th>
                <th className="text-right px-3 py-2">Δ median</th>
              </tr>
            </thead>
            <tbody>
              {[...stats.devs]
                .sort((a, b) => b.elevation_deg - a.elevation_deg)
                .map((d) => (
                  <tr key={d.serial} className="border-t border-gray-800">
                    <td className="px-3 py-1.5 font-mono text-gray-200">{d.serial}</td>
                    <td className="px-3 py-1.5 text-right tabular-nums text-gray-400">
                      {d.elevation_deg}°
                    </td>
                    <td className="px-3 py-1.5 text-right tabular-nums text-gray-200">
                      {(d.level_db as number).toFixed(1)}
                    </td>
                    <td
                      className={`px-3 py-1.5 text-right tabular-nums font-medium ${
                        Math.abs(d.dev) > tolerance ? 'text-red-400' : 'text-emerald-400'
                      }`}
                    >
                      {d.dev >= 0 ? '+' : ''}
                      {d.dev.toFixed(1)}
                    </td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
      )}

      {valid.length > 0 && !allAbsolute && (
        <p className="text-xs text-amber-400">
          ⚠ Some mics have no Sens Factor, so levels are dBFS-relative. Evenness across mics is
          still meaningful only if every mic is calibrated the same way — mixed units make the
          spread misleading.
        </p>
      )}
      <p className="text-xs text-gray-500">
        Broadband RMS, scalar-calibrated, averaged over {avgSec} s in the power domain. The per-frequency response curve is not applied — that
        needs an FIR filter on the time signal, so a mic&apos;s curve shape is invisible here.
      </p>
    </div>
  );
}

function Stat({ label, value, tone }: { label: string; value: string; tone: 'ok' | 'bad' | 'neutral' }) {
  const color = tone === 'bad' ? 'text-red-400' : tone === 'ok' ? 'text-emerald-400' : 'text-gray-200';
  return (
    <div className="bg-gray-900 px-3 py-2">
      <div className="text-[10px] uppercase tracking-wide text-gray-500">{label}</div>
      <div className={`text-lg font-semibold tabular-nums ${color}`}>{value}</div>
    </div>
  );
}
