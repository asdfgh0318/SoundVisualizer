import { useEffect, useState } from 'react';
import { api } from '../../api/client';
import type { TytoStatus as TytoStatusT } from '../../api/types';
import { Button } from '../ui/Button';
import { MotorTest } from './MotorTest';

export function TytoStatus() {
  const [status, setStatus] = useState<TytoStatusT | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [reload, setReload] = useState(0);
  const [busy, setBusy] = useState(false);

  // Poll once on mount, then every 1s — keeps PWM / tare / tripped readouts
  // live so the motor-test progress + cutoff state stay accurate.
  useEffect(() => {
    let cancelled = false;
    const fetchOnce = () =>
      api.tytoStatus().then(
        (s) => !cancelled && setStatus(s),
        (e) => !cancelled && setError(e),
      );
    fetchOnce();
    const id = setInterval(fetchOnce, 1000);
    return () => { cancelled = true; clearInterval(id); };
  }, [reload]);

  const onReset = async () => {
    try {
      await api.resetTytoWatchdog();
      setReload((r) => r + 1);
    } catch (e) {
      setError(e as Error);
    }
  };

  const run = async (fn: () => Promise<unknown>) => {
    setBusy(true);
    setError(null);
    try {
      await fn();
      setReload((r) => r + 1);
    } catch (e) {
      setError(e as Error);
    } finally {
      setBusy(false);
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
  const tared =
    status.tare_thrust_n !== 0 || status.tare_torque_nm !== 0 || status.tare_current_a !== 0;
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

      {/* Tare / zero — the load cell reads a non-zero resting baseline; zero it
          at idle so thrust/torque/current are referenced to rest. */}
      <div className="border-t border-gray-700 pt-2 space-y-1">
        {tared ? (
          <div className="text-xs text-gray-400">
            Tared:{' '}
            <span className="font-mono text-gray-200">
              {status.tare_thrust_n.toFixed(2)} N
            </span>
            {' · '}
            <span className="font-mono text-gray-200">
              {status.tare_torque_nm.toFixed(3)} N·m
            </span>
            {' · '}
            <span className="font-mono text-gray-200">
              {status.tare_current_a.toFixed(2)} A
            </span>
          </div>
        ) : (
          <div className="text-xs text-gray-500">Not tared — readings include resting offset.</div>
        )}
        <div className="flex items-center gap-2">
          <Button onClick={() => run(api.zeroTytoStand)} disabled={busy || status.pwm_us !== 1000}>
            {busy ? 'Zeroing…' : 'Zero stand'}
          </Button>
          {tared && (
            <button
              onClick={() => run(api.clearTytoTare)}
              disabled={busy}
              className="text-xs text-gray-400 hover:text-gray-200 underline disabled:opacity-40"
            >
              clear
            </button>
          )}
        </div>
        {status.pwm_us !== 1000 && (
          <p className="text-[11px] text-amber-400">Spool down to idle (1000 µs) before zeroing.</p>
        )}
      </div>

      {tripped && (
        <Button variant="danger" onClick={onReset}>
          Reset watchdog
        </Button>
      )}

      {/* Direction-check: 4 gentle spool-ups so the user can confirm
          prop-rotation direction matches the expected wiring. */}
      <div className="border-t border-gray-700 pt-2">
        <div className="text-xs uppercase tracking-wide text-gray-500 mb-1">
          Direction check
        </div>
        <MotorTest
          ready={!tripped && status.pwm_us === 1000}
          readyReason={
            tripped
              ? 'Watchdog tripped — reset before running the direction check.'
              : status.pwm_us !== 1000
                ? 'Motor not at idle (PWM ≠ 1000) — spool down before running the direction check.'
                : ''
          }
        />
      </div>
    </div>
  );
}
