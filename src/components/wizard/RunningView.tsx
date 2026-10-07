import type { CaptureRunStatus } from '../../api/types';
import { Button } from '../ui/Button';
import { LiveTelemetry } from './LiveTelemetry';

interface Props {
  status: CaptureRunStatus | null;
  onAbort: () => void;
}

const PHASE_LABELS: Record<string, string> = {
  starting: 'Starting…',
  taring: 'Taring load cells at idle',
  setting_pwm: 'Setting ESC signal',
  stabilizing: 'Waiting for RPM to stabilize',
  recording: 'Recording audio',
  writing: 'Writing measurements',
  repeat_gap: 'Spooling down at 1200 µs before the next repeat',
  spooling_down: 'Spooling motor down',
  completed: 'Completed',
  failed: 'Failed',
  aborted: 'Aborted',
  idle: 'Idle',
};

export function RunningView({ status, onAbort }: Props) {
  const repeats = status?.total_repeats ?? 1;
  const repeatLabel = repeats > 1 ? `Repeat ${status?.current_repeat || 1} of ${repeats} · ` : '';
  const stepLabel = status
    ? status.total_steps > 0
      ? status.phase === 'repeat_gap'
        ? `${repeatLabel}spool-down`
        : `${repeatLabel}Step ${status.current_step} of ${status.total_steps}`
      : 'Initializing'
    : 'Connecting…';
  const pwmLabel = status?.current_pwm_us ? `ESC ${status.current_pwm_us} µs` : '';
  const phaseLabel = status?.phase ? (PHASE_LABELS[status.phase] ?? status.phase) : '—';

  return (
    <div className="space-y-6">
      <div className="bg-gray-800 border border-gray-700 rounded-lg p-6">
        <div className="flex items-center justify-between gap-4">
          <div>
            <div className="text-xs uppercase tracking-wide text-amber-400">Recording</div>
            <div className="text-2xl font-bold text-white mt-1">{stepLabel}</div>
            <div className="text-sm text-gray-400 mt-1">
              {phaseLabel} {pwmLabel && <span className="text-gray-500">· {pwmLabel}</span>}
            </div>
          </div>
          <Button variant="danger" onClick={onAbort}>
            Abort
          </Button>
        </div>
        {status && status.total_steps > 0 && (
          <div className="mt-4">
            <div className="h-2 bg-gray-900 rounded-full overflow-hidden">
              <div
                className="h-full bg-indigo-500 transition-all"
                style={{
                  width: `${progressPct(status)}%`,
                }}
              />
            </div>
          </div>
        )}
        <div className="text-xs text-gray-500 mt-3">
          Measurements written: {status?.measurement_ids.length ?? 0}
        </div>
      </div>

      <LiveTelemetry active />
    </div>
  );
}

function progressPct(status: CaptureRunStatus): number {
  const repeats = Math.max(1, status.total_repeats ?? 1);
  const done = Math.max(0, (status.current_repeat || 1) - 1) * status.total_steps;
  const inPass =
    status.phase === 'repeat_gap'
      ? 0
      : Math.max(0, status.current_step - 1) + phasePct(status.phase) / 100;
  return Math.min(100, ((done + inPass) / (status.total_steps * repeats)) * 100);
}

function phasePct(phase: string): number {
  return (
    {
      taring: 5,
      setting_pwm: 15,
      stabilizing: 30,
      recording: 70,
      writing: 95,
      spooling_down: 100,
    }[phase] ?? 0
  );
}
