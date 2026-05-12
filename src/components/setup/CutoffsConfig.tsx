import { useState } from 'react';
import { api, ApiError } from '../../api/client';
import type { CutoffChannelName } from '../../api/types';
import { useSetupStore } from '../../stores/setupStore';
import { Button } from '../ui/Button';

const CHANNELS: { name: CutoffChannelName; label: string; unit: string }[] = [
  { name: 'current', label: 'Current',     unit: 'A'   },
  { name: 'voltage', label: 'Voltage',     unit: 'V'   },
  { name: 'rpm',     label: 'RPM',         unit: 'RPM' },
  { name: 'thrust',  label: 'Thrust',      unit: 'N'   },
  { name: 'torque',  label: 'Torque',      unit: 'N·m' },
  { name: 'temp0',   label: 'Temp 0 (motor)', unit: '°C' },
  { name: 'temp1',   label: 'Temp 1',      unit: '°C'  },
  { name: 'temp2',   label: 'Temp 2',      unit: '°C'  },
];

export function CutoffsConfig() {
  const cutoffs = useSetupStore((s) => s.cutoffs);
  const setCutoff = useSetupStore((s) => s.setCutoff);
  const resetCutoffs = useSetupStore((s) => s.resetCutoffs);

  const [pushState, setPushState] = useState<'idle' | 'pushing' | 'pushed' | 'error'>('idle');
  const [pushError, setPushError] = useState<string | null>(null);

  const onPush = async () => {
    setPushState('pushing');
    setPushError(null);
    try {
      await api.setTytoCutoffs(cutoffs);
      setPushState('pushed');
      setTimeout(() => setPushState('idle'), 2000);
    } catch (e) {
      setPushError((e as ApiError).message);
      setPushState('error');
    }
  };

  return (
    <div className="space-y-4">
      <table className="w-full text-sm">
        <thead>
          <tr className="text-left text-gray-400 border-b border-gray-700">
            <th className="py-2 pr-3 font-medium w-8"></th>
            <th className="pr-3 font-medium">Channel</th>
            <th className="pr-3 font-medium">Trips when</th>
            <th className="pr-3 font-medium">Threshold</th>
            <th className="font-medium">Unit</th>
          </tr>
        </thead>
        <tbody>
          {CHANNELS.map(({ name, label, unit }) => {
            const c = cutoffs[name];
            return (
              <tr key={name} className="border-b border-gray-700/50 last:border-b-0">
                <td className="py-2 pr-3">
                  <input
                    type="checkbox"
                    checked={c.enabled}
                    onChange={(e) => setCutoff(name, { enabled: e.target.checked })}
                    className="accent-indigo-500 w-4 h-4"
                    aria-label={`Enable ${label} cutoff`}
                  />
                </td>
                <td className="pr-3 text-gray-200">{label}</td>
                <td className="pr-3">
                  <select
                    className="input w-24"
                    value={c.direction}
                    disabled={!c.enabled}
                    onChange={(e) =>
                      setCutoff(name, { direction: e.target.value as 'above' | 'below' })
                    }
                  >
                    <option value="above">↑ above</option>
                    <option value="below">↓ below</option>
                  </select>
                </td>
                <td className="pr-3">
                  <input
                    type="number"
                    className="input w-28"
                    value={c.threshold}
                    disabled={!c.enabled}
                    onChange={(e) => setCutoff(name, { threshold: Number(e.target.value) })}
                  />
                </td>
                <td className="text-gray-400 text-xs">{unit}</td>
              </tr>
            );
          })}
        </tbody>
      </table>

      <div className="flex items-center gap-3 pt-2 border-t border-gray-700/50">
        <Button onClick={onPush} disabled={pushState === 'pushing'}>
          {pushState === 'pushing' ? 'Pushing…' : 'Push to Tyto'}
        </Button>
        <Button variant="ghost" onClick={resetCutoffs}>
          Reset to defaults
        </Button>
        {pushState === 'pushed' && <span className="text-xs text-green-400">Saved.</span>}
        {pushState === 'error' && (
          <span className="text-xs text-red-400">Failed: {pushError}</span>
        )}
      </div>
      <p className="text-xs text-gray-500">
        "Push to Tyto" sends thresholds to the running watchdog. Requires <code className="font-mono">tyto.enabled = true</code> in <code className="font-mono">config.toml</code>.
      </p>
    </div>
  );
}
