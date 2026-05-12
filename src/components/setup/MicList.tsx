import { useEffect, useState } from 'react';
import { api } from '../../api/client';
import type { AudioDeviceInfo, CalibrationSummary, MicConfig } from '../../api/types';
import { ELEVATION_VALUES } from '../../api/types';
import { useSetupStore } from '../../stores/setupStore';
import { Button } from '../ui/Button';
import { PresetControls } from './PresetControls';

export function MicList() {
  const mics = useSetupStore((s) => s.mics);
  const addMic = useSetupStore((s) => s.addMic);
  const updateMic = useSetupStore((s) => s.updateMic);
  const removeMic = useSetupStore((s) => s.removeMic);
  const calibrationsVersion = useSetupStore((s) => s.calibrationsVersion);

  const [devices, setDevices] = useState<AudioDeviceInfo[]>([]);
  const [calibrations, setCalibrations] = useState<CalibrationSummary[]>([]);

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
          onChange={(patch) => updateMic(m.id, patch)}
          onDelete={() => removeMic(m.id)}
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
  onChange,
  onDelete,
}: {
  index: number;
  mic: MicConfig;
  devices: AudioDeviceInfo[];
  calibrations: CalibrationSummary[];
  onChange: (patch: Partial<MicConfig>) => void;
  onDelete: () => void;
}) {
  return (
    <div className="grid grid-cols-12 gap-3 items-center bg-gray-900/40 border border-gray-700 rounded-md p-3">
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
