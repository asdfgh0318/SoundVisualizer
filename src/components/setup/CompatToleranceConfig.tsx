import { useEffect, useState } from 'react';
import { api, ApiError } from '../../api/client';
import type { CompatibilityTolerances } from '../../api/types';
import { COMPAT_CHANNELS } from '../../api/types';
import { Button } from '../ui/Button';

export function CompatToleranceConfig() {
  const [tolerances, setTolerances] = useState<CompatibilityTolerances | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [saveState, setSaveState] = useState<'idle' | 'saving' | 'saved' | 'error'>('idle');
  const [saveError, setSaveError] = useState<string | null>(null);

  useEffect(() => {
    api.getCompatTolerances().then(
      (t) => setTolerances(t),
      (e: Error | ApiError) => setError(e),
    );
  }, []);

  const update = (
    channel: keyof CompatibilityTolerances,
    field: 'abs' | 'rel',
    value: number,
  ) => {
    if (!tolerances) return;
    setTolerances({
      ...tolerances,
      [channel]: { ...tolerances[channel], [field]: value },
    });
  };

  const onSave = async () => {
    if (!tolerances) return;
    setSaveState('saving');
    setSaveError(null);
    try {
      await api.putCompatTolerances(tolerances);
      setSaveState('saved');
      setTimeout(() => setSaveState('idle'), 2000);
    } catch (e) {
      setSaveError((e as ApiError).message);
      setSaveState('error');
    }
  };

  if (error) return <div className="text-sm text-red-400">Error: {error.message}</div>;
  if (!tolerances) return <div className="text-sm text-gray-400 italic">Loading…</div>;

  return (
    <div className="space-y-4">
      <p className="text-xs text-gray-500">
        Top and bottom captures at the same PWM are grouped into one PWM point on the Results
        page when their performance metrics agree within these tolerances. A pair is compatible
        on a channel when <code className="font-mono text-gray-300">|a − b| ≤ max(abs, rel × mean(|a|, |b|))</code>.
      </p>

      <table className="w-full text-sm">
        <thead>
          <tr className="text-left text-gray-400 border-b border-gray-700">
            <th className="py-2 pr-3 font-medium">Channel</th>
            <th className="pr-3 font-medium">Absolute</th>
            <th className="pr-3 font-medium">Relative (fraction)</th>
            <th className="font-medium">Unit</th>
          </tr>
        </thead>
        <tbody>
          {COMPAT_CHANNELS.map(({ key, label, unit }) => {
            const t = tolerances[key];
            return (
              <tr key={key} className="border-b border-gray-700/50 last:border-b-0">
                <td className="py-2 pr-3 text-gray-200">{label}</td>
                <td className="pr-3">
                  <input
                    type="number"
                    min={0}
                    step="any"
                    className="input w-28"
                    value={t.abs}
                    onChange={(e) => update(key, 'abs', Number(e.target.value))}
                  />
                </td>
                <td className="pr-3">
                  <input
                    type="number"
                    min={0}
                    max={1}
                    step={0.01}
                    className="input w-28"
                    value={t.rel}
                    onChange={(e) => update(key, 'rel', Number(e.target.value))}
                  />
                </td>
                <td className="text-gray-400 text-xs">{unit}</td>
              </tr>
            );
          })}
        </tbody>
      </table>

      <div className="flex items-center gap-3 pt-2 border-t border-gray-700/50">
        <Button onClick={onSave} disabled={saveState === 'saving'}>
          {saveState === 'saving' ? 'Saving…' : 'Save tolerances'}
        </Button>
        {saveState === 'saved' && <span className="text-xs text-green-400">Saved.</span>}
        {saveState === 'error' && (
          <span className="text-xs text-red-400">Failed: {saveError}</span>
        )}
        <span className="text-xs text-gray-500 ml-auto">
          Stored in <code className="font-mono">data/compat-tolerances.json</code>.
        </span>
      </div>
    </div>
  );
}
