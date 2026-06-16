import type { CaptureRunStatus } from '../../api/types';
import { Button } from '../ui/Button';
import { LiveTelemetry } from './LiveTelemetry';

interface Props {
  status: CaptureRunStatus | null;
  onAbort: () => void;
}

const PHASE_LABELS: Record<string, string> = {
  starting: 'Starting…',
  setting_pwm: 'Setting PWM',
  stabilizing: 'Waiting for RPM to stabilize',
  recording: 'Recording audio',
  writing: 'Writing measurements',
  spooling_down: 'Spooling motor down',
  completed: 'Completed',
  failed: 'Failed',
  aborted: 'Aborted',
  idle: 'Idle',
};

export function RunningView({ status, onAbort }: Props) {
  const stepLabel = status
    ? status.total_steps > 0
      ? `Step ${status.current_step} of ${status.total_steps}`
      : 'Initializing'
    : 'Connecting…';
  const pwmLabel = status?.current_pwm_us ? `PWM ${status.current_pwm_us} µs` : '';
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
                  width: `${
                    Math.min(100, ((status.current_step - 1) / status.total_steps) * 100 +
                      (phasePct(status.phase) / status.total_steps))
                  }%`,
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

function phasePct(phase: string): number {
  return (
    {
      setting_pwm: 10,
      stabilizing: 30,
      recording: 70,
      writing: 95,
      spooling_down: 100,
    }[phase] ?? 0
  );
}
