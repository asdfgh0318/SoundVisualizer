import { useEffect, useRef, useState } from 'react';
import { api, ApiError } from '../../api/client';
import { Button } from '../ui/Button';

/** Direction-check sequence: 4 short spool-ups to a low PWM, with a hold and
 *  spool-down between each. The visible accel/decel reveals which way the
 *  prop is spinning (the asymmetric prop shape looks different attacking vs
 *  trailing-edge-first), so you can confirm or fix wiring before any real run. */
const TEST_PWM_US = 1080;       // gentle — well below any reasonable cutoff
const HOLD_AT_TEST_MS = 900;    // long enough to see the prop steady
const REST_AT_IDLE_MS = 1200;   // gap between ramps
const RAMP_COUNT = 4;

interface Props {
  /** True when Tyto is connected, not tripped, and at idle (pwm=1000). The
   *  parent computes these from the live TytoStatus. */
  ready: boolean;
  readyReason: string;
}

type Phase = 'idle' | 'confirming' | 'running' | 'aborting';

export function MotorTest({ ready, readyReason }: Props) {
  const [phase, setPhase] = useState<Phase>('idle');
  const [step, setStep] = useState(0);
  const [subPhase, setSubPhase] = useState<'spool-up' | 'spool-down' | 'idle'>('idle');
  const [error, setError] = useState<string | null>(null);
  // Latched cancel flag — checked between steps. Cancelling sets it; the
  // sequence loop sees it and bails. PWM gets force-set to 1000 either way.
  const cancelRef = useRef(false);

  // Safety net: if the user navigates away mid-test, slam PWM to 1000.
  useEffect(() => {
    return () => {
      cancelRef.current = true;
      // Best-effort; we don't await here because the component is going away.
      api.setTytoPwm(1000).catch(() => {});
    };
  }, []);

  async function sleep(ms: number) {
    return new Promise<void>((r) => setTimeout(r, ms));
  }

  async function runSequence() {
    cancelRef.current = false;
    setError(null);
    setPhase('running');
    try {
      for (let i = 1; i <= RAMP_COUNT; i++) {
        if (cancelRef.current) break;
        setStep(i);

        setSubPhase('spool-up');
        await api.setTytoPwm(TEST_PWM_US);
        await sleep(HOLD_AT_TEST_MS);
        if (cancelRef.current) break;

        setSubPhase('spool-down');
        await api.setTytoPwm(1000);
        // Skip the inter-ramp rest after the last one.
        if (i < RAMP_COUNT) {
          setSubPhase('idle');
          await sleep(REST_AT_IDLE_MS);
        }
      }
    } catch (e) {
      const msg = e instanceof ApiError || e instanceof Error ? e.message : String(e);
      setError(`Sequence failed: ${msg}`);
    } finally {
      // Always force idle, even on cancel or error.
      try {
        await api.setTytoPwm(1000);
      } catch {
        // Already in trouble; surfacing this would be confusing.
      }
      setSubPhase('idle');
      setStep(0);
      setPhase('idle');
    }
  }

  const onAbort = () => {
    cancelRef.current = true;
    setPhase('aborting');
  };

  const subPhaseLabel =
    subPhase === 'spool-up' ? 'spooling up'
    : subPhase === 'spool-down' ? 'spooling down'
    : 'resting at idle';

  return (
    <div className="space-y-2">
      <p className="text-xs text-gray-500">
        Runs {RAMP_COUNT} gentle spool-up/down cycles to PWM {TEST_PWM_US} µs so you can
        eyeball which way the prop is turning. Stop with the red button if anything looks wrong.
      </p>

      {phase === 'idle' && (
        <>
          <Button
            onClick={() => setPhase('confirming')}
            disabled={!ready}
            title={ready ? '' : readyReason}
          >
            Run direction check
          </Button>
          {!ready && (
            <p className="text-[11px] text-amber-400">{readyReason}</p>
          )}
        </>
      )}

      {phase === 'confirming' && (
        <div className="bg-amber-500/10 border border-amber-500/40 rounded p-3 space-y-2">
          <p className="text-xs text-amber-200">
            <strong>Prop clear?</strong> The motor will spool to PWM {TEST_PWM_US} µs {RAMP_COUNT} times.
            Make sure nothing is in the prop arc.
          </p>
          <div className="flex gap-2">
            <Button onClick={runSequence}>Start</Button>
            <Button variant="ghost" onClick={() => setPhase('idle')}>Cancel</Button>
          </div>
        </div>
      )}

      {(phase === 'running' || phase === 'aborting') && (
        <div className="bg-gray-900/40 border border-gray-700 rounded p-3 space-y-2">
          <div className="text-xs text-gray-300">
            Ramp <span className="font-mono">{step}/{RAMP_COUNT}</span> · <span className="text-amber-300">{subPhaseLabel}</span>
            {phase === 'aborting' && <span className="ml-2 text-red-300">(aborting…)</span>}
          </div>
          <Button variant="danger" onClick={onAbort} disabled={phase === 'aborting'}>
            Stop
          </Button>
        </div>
      )}

      {error && (
        <p className="text-xs text-red-400">{error}</p>
      )}
    </div>
  );
}
