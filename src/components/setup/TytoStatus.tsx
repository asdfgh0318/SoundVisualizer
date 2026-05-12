import { useEffect, useState } from 'react';
import { api } from '../../api/client';
import type { TytoStatus as TytoStatusT } from '../../api/types';
import { Button } from '../ui/Button';

export function TytoStatus() {
  const [status, setStatus] = useState<TytoStatusT | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [reload, setReload] = useState(0);

  useEffect(() => {
    let cancelled = false;
    api.tytoStatus().then(
      (s) => !cancelled && setStatus(s),
      (e) => !cancelled && setError(e),
    );
    return () => { cancelled = true; };
  }, [reload]);

  const onReset = async () => {
    try {
      await api.resetTytoWatchdog();
      setReload((r) => r + 1);
    } catch (e) {
      setError(e as Error);
    }
  };

  if (error) {
    return <div className="text-sm text-red-400">Error: {error.message}</div>;
  }
  if (!status) return <div className="text-sm text-gray-400 italic">Loading…</div>;

  if (!status.connected) {
    return (
      <div className="text-sm space-y-1">
        <div className="flex items-center gap-2">
          <span className="inline-block w-2 h-2 rounded-full bg-gray-500"></span>
          <span className="text-gray-400">Not connected</span>
        </div>
        <p className="text-xs text-gray-500">
          Set <code className="font-mono">tyto.enabled = true</code> in <code className="font-mono">config.toml</code>{' '}
          and restart the server.
        </p>
      </div>
    );
  }

  const tripped = status.tripped;
  return (
    <div className="text-sm space-y-2">
      <div className="flex items-center gap-2">
        <span
          className={`inline-block w-2 h-2 rounded-full ${tripped ? 'bg-red-500' : 'bg-green-500'}`}
        ></span>
        <span className="text-gray-200">
          {tripped ? `Tripped on ${tripped}` : 'Connected, armed'}
        </span>
      </div>
      <div className="text-xs text-gray-400">
        PWM: <span className="font-mono text-gray-200">{status.pwm_us ?? '—'} µs</span>
      </div>
      {tripped && (
        <Button variant="danger" onClick={onReset}>
          Reset watchdog
        </Button>
      )}
    </div>
  );
}
