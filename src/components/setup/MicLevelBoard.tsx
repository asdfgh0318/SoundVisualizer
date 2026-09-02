import { useEffect, useMemo, useRef, useState } from 'react';
import { WS_BASE } from '../../api/base';
import { api } from '../../api/client';
import type { AudioDeviceInfo } from '../../api/types';
import { useSetupStore } from '../../stores/setupStore';
import { Button } from '../ui/Button';

/** Every mic's level, live, side by side.
 *
 *  UMIK-2s all report USB serial 00000, so the only way to tell which physical
 *  mic is which is to tap one and see which row moves. Showing every device at
 *  once — including ones no mic row is bound to — means one pass of tapping
 *  identifies the whole arc, and a mic bound to the wrong elevation shows up as
 *  the wrong row moving.
 *
 *  Peak-hold matters here: a tap is a transient, and at 10 frames/sec a bar
 *  that only shows the instantaneous level can return to rest before you have
 *  looked up from the mic. */

const HOLD_MS = 1500;
const FLOOR_DB = -90; // bar scale bottom, dBFS-ish; taps land far above this

interface Frame {
  serial: string; // we send alsa_card_id as the key
  level_db: number | null;
}

interface Row {
  card: string;
  index: number;
  level: number | null;
  peak: number | null;
  peakAt: number;
}

export function MicLevelBoard() {
  const mics = useSetupStore((s) => s.mics);
  const updateMic = useSetupStore((s) => s.updateMic);

  const [devices, setDevices] = useState<AudioDeviceInfo[]>([]);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [rows, setRows] = useState<Row[]>([]);
  const peaks = useRef<Map<string, { db: number; at: number }>>(new Map());

  useEffect(() => {
    api.listAudioDevices().then(setDevices, () => setDevices([]));
  }, []);

  /** Which mic row (if any) currently claims each card. */
  const boundTo = useMemo(() => {
    const m = new Map<string, { elev: number | null; serial: string; id: string }>();
    for (const mic of mics) {
      if (mic.alsaCardId) m.set(mic.alsaCardId, { elev: mic.elevationDeg, serial: mic.serial, id: mic.id });
    }
    return m;
  }, [mics]);

  useEffect(() => {
    if (!running || devices.length === 0) return;
    const ws = new WebSocket(`${WS_BASE}/devices/audio/levels`);
    setError(null);
    peaks.current = new Map();

    ws.onopen = () =>
      ws.send(
        JSON.stringify({
          mics: devices.map((d) => ({
            serial: d.alsa_card_id ?? `idx${d.index}`,
            device_index: d.index,
            elevation_deg: 0,
            calibration_file_id: null,
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
      const frames: Frame[] = msg.levels ?? [];
      const now = Date.now();
      const next: Row[] = frames.map((f) => {
        const lvl = f.level_db !== null && Number.isFinite(f.level_db) ? f.level_db : null;
        const held = peaks.current.get(f.serial);
        if (lvl !== null && (!held || lvl > held.db || now - held.at > HOLD_MS)) {
          peaks.current.set(f.serial, { db: lvl, at: now });
        }
        const p = peaks.current.get(f.serial);
        const dev = devices.find((d) => (d.alsa_card_id ?? `idx${d.index}`) === f.serial);
        return {
          card: f.serial,
          index: dev?.index ?? -1,
          level: lvl,
          peak: p ? p.db : null,
          peakAt: p ? p.at : 0,
        };
      });
      setRows(next);
    };

    ws.onerror = () => setError('connection failed');
    ws.onclose = (e) => {
      if (e.code === 1011) setError(e.reason || 'refused — is a capture running?');
      setRunning(false);
    };
    return () => ws.close();
  }, [running, devices]);

  const pct = (db: number | null) =>
    db === null ? 0 : Math.max(0, Math.min(100, ((db - FLOOR_DB) / (0 - FLOOR_DB)) * 100));

  const sorted = useMemo(
    () =>
      [...rows].sort((a, b) => {
        const ea = boundTo.get(a.card)?.elev;
        const eb = boundTo.get(b.card)?.elev;
        if (ea == null && eb == null) return a.card.localeCompare(b.card);
        if (ea == null) return 1;
        if (eb == null) return -1;
        return eb - ea;
      }),
    [rows, boundTo],
  );

  const assignTo = (card: string, micId: string) => {
    const dev = devices.find((d) => (d.alsa_card_id ?? `idx${d.index}`) === card);
    if (dev) updateMic(micId, { deviceIndex: dev.index, alsaCardId: dev.alsa_card_id ?? null });
  };

  return (
    <div className="space-y-3">
      <p className="text-xs text-gray-500">
        Tap a mic and watch which row jumps. Peak is held for {HOLD_MS / 1000}s so a tap is still
        visible after you look up. Every present device is listed, including any no row is bound to.
        Cannot run during a capture — a device can&apos;t be opened twice.
      </p>

      <div className="flex flex-wrap items-center gap-3">
        <Button
          onClick={() => setRunning((r) => !r)}
          variant={running ? 'danger' : 'primary'}
          disabled={devices.length === 0}
        >
          {running ? 'Stop' : `Start live levels (${devices.length} devices)`}
        </Button>
      </div>

      {error && <p className="text-xs text-red-400">⚠ {error}</p>}

      {sorted.length > 0 && (
        <div className="space-y-1">
          {sorted.map((r) => {
            const bound = boundTo.get(r.card);
            return (
              <div
                key={r.card}
                className="flex items-center gap-2 px-2 py-1.5 rounded border border-gray-800"
              >
                <span className="font-mono text-xs text-gray-300 w-36 shrink-0 truncate">
                  {r.card}
                </span>
                <span className="text-xs w-20 shrink-0 tabular-nums">
                  {bound ? (
                    <span className="text-gray-300">
                      {bound.elev !== null ? `${bound.elev > 0 ? '+' : ''}${bound.elev}°` : '—'}
                      <span className="text-gray-600"> {bound.serial}</span>
                    </span>
                  ) : (
                    <span className="text-amber-400">unbound</span>
                  )}
                </span>

                <div className="relative flex-1 h-4 bg-gray-900 rounded overflow-hidden">
                  <div
                    className="absolute inset-y-0 left-0 bg-indigo-400"
                    style={{ width: `${pct(r.level)}%` }}
                  />
                  {r.peak !== null && (
                    <div
                      className="absolute inset-y-0 w-0.5 bg-amber-400"
                      style={{ left: `${pct(r.peak)}%` }}
                      title="peak hold"
                    />
                  )}
                </div>

                <span className="font-mono text-xs text-gray-400 w-14 text-right tabular-nums">
                  {r.level === null ? '—' : r.level.toFixed(0)}
                </span>

                <select
                  className="input py-0.5 text-xs w-28"
                  value={bound?.id ?? ''}
                  onChange={(e) => e.target.value && assignTo(r.card, e.target.value)}
                  title="Assign this device to a mic row"
                >
                  <option value="">assign to…</option>
                  {mics.map((m) => (
                    <option key={m.id} value={m.id}>
                      {m.elevationDeg !== null ? `${m.elevationDeg}° ` : ''}
                      {m.serial}
                    </option>
                  ))}
                </select>
              </div>
            );
          })}
        </div>
      )}

      {running && rows.length === 0 && (
        <p className="text-sm text-gray-500">waiting for the first frame…</p>
      )}
    </div>
  );
}
