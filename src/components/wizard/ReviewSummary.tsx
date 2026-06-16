import type { MicConfig } from '../../api/types';
import type { WizardForm } from '../../stores/wizardStore';
import { Button } from '../ui/Button';
import { Card } from '../ui/Card';

interface Props {
  form: WizardForm;
  mics: MicConfig[];
  cutoffsConfigured: boolean;
  fakeRunning: boolean;
  onBack: () => void;
  onConfirm: () => void;
  onFakeRun: () => void;
}

export function ReviewSummary({
  form,
  mics,
  cutoffsConfigured,
  fakeRunning,
  onBack,
  onConfirm,
  onFakeRun,
}: Props) {
  const selectedMics = mics.filter(
    (m) => m.serial && m.deviceIndex !== null && form.selected_mic_ids.includes(m.id),
  );
  const totalRecordingS =
    form.pwm_steps.reduce((sum, s) => sum + s.recording_ms, 0) / 1000;

  return (
    <Card title="Review" description="Confirm before motor spool-up.">
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 text-sm">
        <Section label="Storage key">
          <div className="font-mono text-gray-200">
            {[form.motor, form.propeller, form.shroud, form.notes]
              .map((s) => s.trim() || '∅')
              .join(' · ')}
          </div>
        </Section>
        <Section label="Capture mode">
          <div className="text-gray-200">
            Single-pass <span className="text-gray-500">(all mics record simultaneously)</span>
          </div>
        </Section>
        <Section label="PWM ramp">
          <ul className="text-gray-300 space-y-0.5">
            {form.pwm_steps.map((s, i) => (
              <li key={i} className="font-mono">
                {s.pwm_us} µs · record {s.recording_ms} ms
              </li>
            ))}
          </ul>
        </Section>
        <Section label="Capture">
          <div className="text-gray-300">
            {form.sample_rate} Hz sample rate
            <br />
            {totalRecordingS.toFixed(2)}s total recording (+ stabilize time per step)
          </div>
        </Section>
        <Section label={`Microphones (${selectedMics.length})`}>
          <ul className="text-gray-300 text-xs space-y-0.5">
            {selectedMics.map((m) => (
              <li key={m.id} className="font-mono">
                {m.serial} · device #{m.deviceIndex} · elev {m.elevationDeg ?? '—'}°
              </li>
            ))}
          </ul>
        </Section>
        <Section label="Trigger sync">
          <div className="text-gray-300">
            {form.trigger.enabled
              ? `${form.trigger.threshold_db} dBFS, block ${form.trigger.block_size}, preroll ${form.trigger.preroll_samples}`
              : 'disabled'}
          </div>
        </Section>
      </div>

      {!cutoffsConfigured && (
        <div className="mt-4 p-3 rounded-md border border-amber-700/60 bg-amber-900/20 text-amber-300 text-sm">
          ⚠ No safety cutoffs are enabled. The watchdog will not stop the motor on overcurrent /
          overheat. You can configure them on the <strong>Setup</strong> page.
        </div>
      )}

      <div className="flex items-center justify-between gap-3 mt-6 pt-4 border-t border-gray-700">
        <Button variant="secondary" onClick={onFakeRun} disabled={fakeRunning}>
          {fakeRunning ? 'Generating…' : '✦ Run fake capture (skip hardware)'}
        </Button>
        <div className="flex items-center gap-3">
          <Button variant="ghost" onClick={onBack}>
            ← Back
          </Button>
          <Button onClick={onConfirm}>Start capture →</Button>
        </div>
      </div>
    </Card>
  );
}

function Section({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div>
      <div className="text-xs uppercase tracking-wide text-gray-500 mb-1">{label}</div>
      {children}
    </div>
  );
}
