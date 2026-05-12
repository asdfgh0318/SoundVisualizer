import { Button } from '../ui/Button';
import { PWMRampVisualization } from './PWMRampVisualization';

interface Step {
  pwm_us: number;
  recording_ms: number;
}

interface Props {
  steps: Step[];
  onChange: (steps: Step[]) => void;
}

export function PWMRampEditor({ steps, onChange }: Props) {
  const update = (i: number, patch: Partial<Step>) =>
    onChange(steps.map((s, j) => (i === j ? { ...s, ...patch } : s)));
  const remove = (i: number) => onChange(steps.filter((_, j) => j !== i));
  const add = () => {
    const last = steps[steps.length - 1];
    onChange([
      ...steps,
      {
        pwm_us: Math.min(2000, (last?.pwm_us ?? 1200) + 100),
        recording_ms: last?.recording_ms ?? 1000,
      },
    ]);
  };

  return (
    <div className="space-y-3">
      <PWMRampVisualization steps={steps} />

      <table className="w-full text-sm">
        <thead>
          <tr className="text-left text-gray-400 border-b border-gray-700">
            <th className="py-1.5 pr-3 font-medium w-12">#</th>
            <th className="pr-3 font-medium">PWM (µs)</th>
            <th className="pr-3 font-medium">Recording duration (ms)</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {steps.map((s, i) => (
            <tr key={i} className="border-b border-gray-700/50 last:border-b-0">
              <td className="py-1.5 pr-3 font-mono text-gray-400">{i + 1}</td>
              <td className="pr-3">
                <input
                  type="number"
                  min={1000}
                  max={2000}
                  step={10}
                  className="input w-28"
                  value={s.pwm_us}
                  onChange={(e) => update(i, { pwm_us: Number(e.target.value) })}
                />
              </td>
              <td className="pr-3">
                <input
                  type="number"
                  min={100}
                  max={60000}
                  step={100}
                  className="input w-32"
                  value={s.recording_ms}
                  onChange={(e) => update(i, { recording_ms: Number(e.target.value) })}
                />
              </td>
              <td className="text-right">
                <button
                  onClick={() => remove(i)}
                  disabled={steps.length === 1}
                  className="text-gray-500 hover:text-red-400 disabled:opacity-40"
                  aria-label={`Remove step ${i + 1}`}
                >
                  ✕
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <Button variant="secondary" onClick={add}>
        + Add step
      </Button>
      <p className="text-xs text-gray-500">
        Each step: drive Tyto to the configured PWM, wait for RPM to stabilize, then record audio
        for the specified duration.
      </p>
    </div>
  );
}
