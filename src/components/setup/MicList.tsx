import { useEffect, useState } from 'react';
import { WS_BASE } from '../../api/base';
import { api } from '../../api/client';
import type { AudioDeviceInfo, CalibrationSummary, MicConfig } from '../../api/types';
import { ELEVATION_VALUES } from '../../api/types';
import { useWebSocketJson } from '../../hooks/useWebSocketJson';
import { useSetupStore } from '../../stores/setupStore';
import { Button } from '../ui/Button';
import { PresetControls } from './PresetControls';

interface LevelFrame {
  rms_dbfs: number;
  peak_dbfs: number;
  overflow?: boolean;
  error?: string;
}

export function MicList() {
  const mics = useSetupStore((s) => s.mics);
  const addMic = useSetupStore((s) => s.addMic);
  const updateMic = useSetupStore((s) => s.updateMic);
  const removeMic = useSetupStore((s) => s.removeMic);
  const calibrationsVersion = useSetupStore((s) => s.calibrationsVersion);

  const [devices, setDevices] = useState<AudioDeviceInfo[]>([]);
  const [calibrations, setCalibrations] = useState<CalibrationSummary[]>([]);
  // Only one row may listen at a time — a device can't be opened twice.
  const [listeningId, setListeningId] = useState<string | null>(null);

  useEffect(() => {
    api.listAudioDevices().then(setDevices, () => setDevices([]));
  }, []);

  useEffect(() => {
    api.listCalibrations().then(setCalibrations, () => setCalibrations([]));
  }, [calibrationsVersion]);

  return (
    <div className="space-y-3">
      <PresetControls />
      <div className="hidden sm:grid grid-cols-12 gap-3 text-[11px] uppercase tracking-wide text-gray-500 px-1">
        <div className="col-span-1">#</div>
        <div className="col-span-2">Serial</div>
        <div className="col-span-3">USB device</div>
        <div className="col-span-2">Top elev.</div>
        <div className="col-span-2">Bottom elev.</div>
        <div className="col-span-2">Calibration</div>
      </div>
      {mics.length === 0 && (
        <p className="text-sm text-gray-400 italic">
          No microphones yet. Click <span className="text-gray-200">Add microphone</span> to start.
        </p>
      )}
      {mics.map((m, i) => (
        <MicRow
          key={m.id}
          index={i}
          mic={m}
          devices={devices}
          calibrations={calibrations}
          isListening={listeningId === m.id}
          onToggleListen={() => setListeningId((cur) => (cur === m.id ? null : m.id))}
          onChange={(patch) => updateMic(m.id, patch)}
          onDelete={() => {
            if (listeningId === m.id) setListeningId(null);
            removeMic(m.id);
          }}
        />
      ))}
      <div className="pt-2 flex items-center gap-3">
        <Button onClick={addMic}>+ Add microphone</Button>
        <span className="text-xs text-gray-500">{mics.length} mic{mics.length === 1 ? '' : 's'} configured</span>
      </div>
    </div>
  );
}

function MicRow({
  index,
  mic,
  devices,
  calibrations,
  isListening,
  onToggleListen,
  onChange,
  onDelete,
}: {
  index: number;
  mic: MicConfig;
  devices: AudioDeviceInfo[];
  calibrations: CalibrationSummary[];
  isListening: boolean;
  onToggleListen: () => void;
  onChange: (patch: Partial<MicConfig>) => void;
  onDelete: () => void;
}) {
  const hasDevice = mic.deviceIndex !== null;

  return (
    <div className="bg-gray-900/40 border border-gray-700 rounded-md p-3 space-y-2">
      <div className="grid grid-cols-12 gap-3 items-center">
        <div className="col-span-1 font-mono text-gray-400 text-sm">#{index + 1}</div>

        <input
          className="col-span-2 input"
          placeholder="serial"
          value={mic.serial}
          onChange={(e) => onChange({ serial: e.target.value })}
        />

        <select
          className="col-span-3 input"
          value={mic.deviceIndex ?? ''}
          onChange={(e) =>
            onChange({ deviceIndex: e.target.value === '' ? null : Number(e.target.value) })
          }
        >
          <option value="">— pick device —</option>
          {devices.map((d) => (
            <option key={d.index} value={d.index}>
              #{d.index} · {d.name}
            </option>
          ))}
        </select>

        <ElevationSelect
          className="col-span-2"
          value={mic.topElevationDeg}
          onChange={(v) => onChange({ topElevationDeg: v })}
          values={TOP_ELEVATIONS}
        />
        <ElevationSelect
          className="col-span-2"
          value={mic.bottomElevationDeg}
          onChange={(v) => onChange({ bottomElevationDeg: v })}
          values={BOTTOM_ELEVATIONS}
        />

        <select
          className="col-span-1 input"
          value={mic.calibrationFileId ?? ''}
          onChange={(e) =>
            onChange({ calibrationFileId: e.target.value === '' ? null : e.target.value })
          }
        >
          <option value="">none</option>
          {calibrations.map((c) => (
            <option key={c.id} value={c.id}>
              {c.id}
            </option>
          ))}
        </select>

        <div className="col-span-1 flex justify-end">
          <button
            onClick={onDelete}
            className="text-gray-500 hover:text-red-400 text-sm"
            aria-label={`Delete mic ${index + 1}`}
          >
            ✕
          </button>
        </div>
      </div>

      {/* Listen row — tap the mic and watch the bar to identify which physical
          UMIK-2 this device is (they all report the same USB serial). */}
      <div className="flex items-center gap-3">
        <button
          onClick={onToggleListen}
          disabled={!hasDevice}
          className={`shrink-0 text-xs font-medium rounded px-2 py-1 border transition-colors ${
            isListening
              ? 'border-emerald-500 text-emerald-300 bg-emerald-500/10'
              : 'border-gray-600 text-gray-300 hover:border-gray-500 disabled:opacity-40 disabled:cursor-not-allowed'
          }`}
          title={hasDevice ? 'Live input level' : 'Pick a USB device first'}
        >
          {isListening ? '◼ Stop' : '🎤 Listen'}
        </button>
        {isListening && mic.deviceIndex !== null ? (
          <LevelMeter deviceIndex={mic.deviceIndex} />
        ) : (
          <span className="text-[11px] text-gray-600">
            {hasDevice ? 'tap the mic to see its level move' : 'no device selected'}
          </span>
        )}
      </div>
    </div>
  );
}

/** Live RMS/peak level bar fed by /devices/audio/{index}/level over WS.
 *  dBFS in [FLOOR, 0] maps to bar width [0%, 100%]. */
function LevelMeter({ deviceIndex }: { deviceIndex: number }) {
  const FLOOR = -60;
  const url = `${WS_BASE}/devices/audio/${deviceIndex}/level`;
  const { message, state } = useWebSocketJson<LevelFrame>(url, true);

  if (message?.error) {
    return <span className="text-[11px] text-red-400">error: {message.error}</span>;
  }
  if (state === 'connecting' || !message) {
    return <span className="text-[11px] text-gray-500 italic">opening stream…</span>;
  }

  const pct = (db: number) => Math.max(0, Math.min(100, ((db - FLOOR) / -FLOOR) * 100));
  const rmsPct = pct(message.rms_dbfs);
  const peakPct = pct(message.peak_dbfs);

  return (
    <div className="flex items-center gap-2 flex-1 min-w-0">
      <div className="relative h-3 flex-1 min-w-0 rounded bg-gray-800 overflow-hidden">
        <div
          className="absolute inset-y-0 left-0 rounded-l"
          style={{
            width: `${rmsPct}%`,
            background:
              'linear-gradient(to right, hsl(140,70%,45%), hsl(80,70%,48%) 65%, hsl(0,75%,55%))',
          }}
        />
        {/* peak-hold tick */}
        <div
          className="absolute inset-y-0 w-0.5 bg-gray-200"
          style={{ left: `calc(${peakPct}% - 1px)` }}
        />
      </div>
      <span
        className={`text-[11px] font-mono tabular-nums w-16 text-right ${
          message.overflow ? 'text-red-400' : 'text-gray-400'
        }`}
      >
        {message.rms_dbfs <= FLOOR ? '−∞' : message.rms_dbfs.toFixed(1)} dB
      </span>
    </div>
  );
}

// Top mics live above the prop plane → 0° to +90°. Bottom below → -90° to 0°.
// 0° belongs in both since the equator mic may not be physically remounted.
const TOP_ELEVATIONS = ELEVATION_VALUES.filter((v) => v >= 0);
const BOTTOM_ELEVATIONS = ELEVATION_VALUES.filter((v) => v <= 0);

function ElevationSelect({
  value,
  onChange,
  values,
  className = '',
}: {
  value: number | null;
  onChange: (v: number | null) => void;
  values: readonly number[];
  className?: string;
}) {
  return (
    <select
      className={`${className} input`}
      value={value ?? ''}
      onChange={(e) => onChange(e.target.value === '' ? null : Number(e.target.value))}
    >
      <option value="">— °</option>
      {values.map((v) => (
        <option key={v} value={v}>
          {v > 0 ? `+${v}` : v}°
        </option>
      ))}
    </select>
  );
}
