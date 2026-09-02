import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { WS_BASE } from '../../api/base';
import { api } from '../../api/client';
import type { AudioDeviceInfo } from '../../api/types';
import { useSetupStore } from '../../stores/setupStore';
import { Button } from '../ui/Button';

/** Walk the arc, tap each mic, record which device actually responded.
 *
 *  UMIK-2s all report USB serial 00000, so nothing in software can tell them
 *  apart — the only ground truth is which one moves when you tap it. This
 *  streams EVERY present device rather than the saved mic rows, so it can
 *  rebuild the mapping from scratch and is not misled by a preset that is
 *  already wrong (which is exactly how a wrong calibration curve gets applied
 *  to an elevation without anyone noticing). */

interface Frame {
  serial: string; // we send alsa_card_id here, so frames come back keyed by card
  level_db: number | null;
}

/** A tap must clear this much above the mic's own quiet baseline... */
const RISE_DB = 12;
/** ...and beat the second-loudest riser by this much, so one tap picks one mic. */
const MARGIN_DB = 6;
const BASELINE_FRAMES = 20;

export function MicIdentifyWizard() {
  const mics = useSetupStore((s) => s.mics);
  const updateMic = useSetupStore((s) => s.updateMic);

  const [devices, setDevices] = useState<AudioDeviceInfo[]>([]);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [stepIdx, setStepIdx] = useState(0);
  const [found, setFound] = useState<Record<number, string>>({}); // elevation -> alsa_card_id
  const [levels, setLevels] = useState<Record<string, number>>({});
  const [armed, setArmed] = useState(false);

  const baselines = useRef<Map<string, number[]>>(new Map());
  const stepRef = useRef(0);
  const foundRef = useRef<Record<number, string>>({});
  const armedRef = useRef(false);

  useEffect(() => {
    api.listAudioDevices().then(setDevices, () => setDevices([]));
  }, []);

  // The arc to walk: whatever elevations are configured, high to low.
  const steps = useMemo(
    () =>
      mics
        .filter((m) => m.elevationDeg !== null)
        .map((m) => ({ elev: m.elevationDeg as number, serial: m.serial, id: m.id }))
        .sort((a, b) => b.elev - a.elev),
    [mics],
  );

  const expectedCard = useCallback(
    (elev: number) => mics.find((m) => m.elevationDeg === elev)?.alsaCardId ?? null,
    [mics],
  );

  useEffect(() => {
    if (!running) return;
    const ws = new WebSocket(`${WS_BASE}/devices/audio/levels`);
    setError(null);
    baselines.current = new Map();

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
      const now: Record<string, number> = {};
      const rises: { card: string; rise: number }[] = [];

      for (const f of frames) {
        if (f.level_db === null || !Number.isFinite(f.level_db)) continue;
        now[f.serial] = f.level_db;
        const hist = baselines.current.get(f.serial) ?? [];
        if (hist.length >= BASELINE_FRAMES) {
          const quiet = [...hist].sort((a, b) => a - b)[Math.floor(hist.length / 2)];
          rises.push({ card: f.serial, rise: f.level_db - quiet });
        }
        hist.push(f.level_db);
        if (hist.length > BASELINE_FRAMES * 3) hist.shift();
        baselines.current.set(f.serial, hist);
      }
      setLevels(now);

      if (!armedRef.current) return;
      rises.sort((a, b) => b.rise - a.rise);
      const top = rises[0];
      const second = rises[1];
      if (!top || top.rise < RISE_DB) return;
      if (second && top.rise - second.rise < MARGIN_DB) return; // ambiguous — ignore

      const step = steps[stepRef.current];
      if (!step) return;
      foundRef.current = { ...foundRef.current, [step.elev]: top.card };
      setFound(foundRef.current);
      armedRef.current = false;
      setArmed(false);
      baselines.current = new Map(); // fresh baselines for the next mic
      const next = stepRef.current + 1;
      stepRef.current = next;
      setStepIdx(next);
    };

    ws.onerror = () => setError('connection failed');
    ws.onclose = (e) => {
      if (e.code === 1011) setError(e.reason || 'refused — is a capture running?');
      setRunning(false);
      setArmed(false);
      armedRef.current = false;
    };
    return () => ws.close();
  }, [running, devices, steps]);

  const start = () => {
    stepRef.current = 0;
    foundRef.current = {};
    setStepIdx(0);
    setFound({});
    setRunning(true);
  };

  const arm = () => {
    armedRef.current = true;
    setArmed(true);
  };

  const applyAll = () => {
    for (const [elevStr, card] of Object.entries(found)) {
      const elev = Number(elevStr);
      const row = mics.find((m) => m.elevationDeg === elev);
      const dev = devices.find((d) => d.alsa_card_id === card);
      if (row && dev) updateMic(row.id, { deviceIndex: dev.index, alsaCardId: card });
    }
  };

  const done = stepIdx >= steps.length && steps.length > 0;
  const current = steps[stepIdx];
  const mismatches = Object.entries(found).filter(
    ([elev, card]) => expectedCard(Number(elev)) !== card,
  );

  return (
    <div className="space-y-3">
      <p className="text-xs text-gray-500">
        Every UMIK-2 reports serial <code>00000</code>, so tapping is the only way to know which
        mic is which. Walk the arc, tap each mic, and this records the device that actually
        responded — then compare against what Setup currently believes.
      </p>

      {steps.length === 0 && (
        <p className="text-xs text-amber-400">
          No mics with an elevation set. Add rows in the mic list first.
        </p>
      )}

      {!running && steps.length > 0 && (
        <Button onClick={start}>Start tap check ({steps.length} mics)</Button>
      )}

      {running && !done && current && (
        <div className="bg-gray-900/60 border border-indigo-500/40 rounded p-3 space-y-2">
          <div className="text-sm text-gray-200">
            Tap the mic at{' '}
            <span className="font-mono text-lg text-indigo-300">
              {current.elev > 0 ? '+' : ''}
              {current.elev}°
            </span>{' '}
            <span className="text-gray-500">
              ({stepIdx + 1} of {steps.length}, expects{' '}
              <span className="font-mono">{expectedCard(current.elev) ?? '—'}</span>)
            </span>
          </div>
          {armed ? (
            <p className="text-xs text-emerald-400">Listening — tap it now.</p>
          ) : (
            <Button onClick={arm}>Arm and tap</Button>
          )}
          <div className="flex gap-2">
            <Button variant="ghost" onClick={() => { const n = stepIdx + 1; stepRef.current = n; setStepIdx(n); armedRef.current = false; setArmed(false); }}>
              Skip
            </Button>
            <Button variant="danger" onClick={() => setRunning(false)}>Stop</Button>
          </div>
        </div>
      )}

      {running && !armed && Object.keys(levels).length > 0 && (
        <div className="text-[11px] font-mono text-gray-500 flex flex-wrap gap-x-3">
          {Object.entries(levels)
            .sort()
            .map(([c, v]) => (
              <span key={c}>
                {c.replace('umik_', '')}:{v.toFixed(0)}
              </span>
            ))}
        </div>
      )}

      {Object.keys(found).length > 0 && (
        <div className="overflow-x-auto border border-gray-700 rounded">
          <table className="w-full text-xs min-w-[26rem]">
            <thead>
              <tr className="bg-gray-800 text-gray-400 uppercase tracking-wide">
                <th className="text-left px-2 py-1.5">Elev</th>
                <th className="text-left px-2 py-1.5">Expected</th>
                <th className="text-left px-2 py-1.5">Tapped</th>
                <th className="text-left px-2 py-1.5">Verdict</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(found)
                .sort((a, b) => Number(b[0]) - Number(a[0]))
                .map(([elev, card]) => {
                  const exp = expectedCard(Number(elev));
                  const same = exp === card;
                  return (
                    <tr key={elev} className="border-t border-gray-800">
                      <td className="px-2 py-1 font-mono text-gray-200">{elev}°</td>
                      <td className="px-2 py-1 font-mono text-gray-500">{exp ?? '—'}</td>
                      <td className="px-2 py-1 font-mono text-gray-200">{card}</td>
                      <td className={`px-2 py-1 ${same ? 'text-emerald-400' : 'text-red-400'}`}>
                        {same ? 'matches' : 'MISMATCH'}
                      </td>
                    </tr>
                  );
                })}
            </tbody>
          </table>
        </div>
      )}

      {done && (
        <div className="space-y-2">
          <p className={`text-xs ${mismatches.length ? 'text-red-400' : 'text-emerald-400'}`}>
            {mismatches.length
              ? `${mismatches.length} elevation(s) bound to the wrong device.`
              : 'All tapped mics match what Setup expects.'}
          </p>
          {mismatches.length > 0 && (
            <Button onClick={applyAll}>Apply tapped mapping to the mic list</Button>
          )}
        </div>
      )}

      {error && <p className="text-xs text-red-400">⚠ {error}</p>}
    </div>
  );
}
