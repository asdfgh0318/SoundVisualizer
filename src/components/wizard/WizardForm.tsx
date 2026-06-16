import { useEffect } from 'react';
import { useSetupStore } from '../../stores/setupStore';
import { useWizardStore } from '../../stores/wizardStore';
import { Button } from '../ui/Button';
import { Card } from '../ui/Card';
import { KeyFieldsForm } from './KeyFieldsForm';
import { MicSelector } from './MicSelector';
import { PWMRampEditor } from './PWMRampEditor';

interface WizardFormProps {
  fakeRunning: boolean;
  onFakeRun: () => void;
}

export function WizardForm({ fakeRunning, onFakeRun }: WizardFormProps) {
  const form = useWizardStore((s) => s.form);
  const updateForm = useWizardStore((s) => s.updateForm);
  const setPhase = useWizardStore((s) => s.setPhase);
  const mics = useSetupStore((s) => s.mics);

  // Auto-select all mics on first render if none selected.
  useEffect(() => {
    if (form.selected_mic_ids.length === 0 && mics.length > 0) {
      updateForm({ selected_mic_ids: mics.map((m) => m.id) });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [mics.length]);

  const usableMics = mics.filter(
    (m) => m.serial && m.deviceIndex !== null && form.selected_mic_ids.includes(m.id),
  );

  const baseFilled =
    form.motor.trim() !== '' &&
    form.propeller.trim() !== '' &&
    form.pwm_steps.length > 0;

  // Real capture requires fully-configured mics (USB device + serial).
  const canContinue = baseFilled && usableMics.length > 0;

  // Fake capture doesn't need hardware-bound mics.
  const canFakeRun = baseFilled && !fakeRunning;

  return (
    <div className="space-y-6">
      <Card title="Test article" description="Becomes the storage key motor__propeller__shroud__notes.">
        <KeyFieldsForm form={form} onChange={updateForm} />
      </Card>

      <Card title="PWM ramp" description="One acoustic + one performance measurement saved per step.">
        <PWMRampEditor
          steps={form.pwm_steps}
          onChange={(s) => updateForm({ pwm_steps: s })}
        />
      </Card>

      <Card title="Capture settings">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <Labeled label="Sample rate (Hz)">
            <select
              className="input w-full"
              value={form.sample_rate}
              onChange={(e) => updateForm({ sample_rate: Number(e.target.value) })}
            >
              <option value={48000}>48 000</option>
              <option value={44100}>44 100</option>
            </select>
          </Labeled>
        </div>
        <p className="text-xs text-gray-500 mt-3">
          Single-pass capture: every configured mic records simultaneously. Recording duration
          per step is configured in the PWM ramp above.
        </p>
      </Card>

      <Card title="Microphones" description="Pick which configured mics to record this run.">
        <MicSelector
          mics={mics}
          selectedIds={form.selected_mic_ids}
          onChange={(ids) => updateForm({ selected_mic_ids: ids })}
        />
      </Card>

      <Card title="Advanced">
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <Labeled label="Stabilize window (samples)">
            <input
              type="number"
              min={1}
              className="input w-full"
              value={form.stabilize_window}
              onChange={(e) => updateForm({ stabilize_window: Number(e.target.value) })}
            />
          </Labeled>
          <Labeled label="Stabilize tolerance (RPM)">
            <input
              type="number"
              min={0.1}
              step={0.1}
              className="input w-full"
              value={form.stabilize_tolerance}
              onChange={(e) => updateForm({ stabilize_tolerance: Number(e.target.value) })}
            />
          </Labeled>
          <Labeled label="Stabilize timeout (s)">
            <input
              type="number"
              min={1}
              className="input w-full"
              value={form.stabilize_timeout_seconds}
              onChange={(e) => updateForm({ stabilize_timeout_seconds: Number(e.target.value) })}
            />
          </Labeled>
          <Labeled label="Trigger sync">
            <CheckboxLabel
              label={form.trigger.enabled ? 'Enabled' : 'Disabled'}
              checked={form.trigger.enabled}
              onChange={(v) =>
                updateForm({ trigger: { ...form.trigger, enabled: v } })
              }
            />
          </Labeled>
        </div>
      </Card>

      <div className="flex items-center justify-between gap-3 pt-2 border-t border-gray-700">
        <Button variant="secondary" onClick={onFakeRun} disabled={!canFakeRun}>
          {fakeRunning ? 'Generating…' : '✦ Run fake capture (no hardware)'}
        </Button>
        <Button onClick={() => setPhase('review')} disabled={!canContinue}>
          Continue → Review
        </Button>
      </div>
      {!canContinue && baseFilled && (
        <p className="text-xs text-gray-500 -mt-2">
          To start a real capture, configure at least one mic with a USB device on the Setup page.
          The fake capture works with the elevations you've set, or default ones if none.
        </p>
      )}
    </div>
  );
}

function Labeled({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <label className="block">
      <span className="text-xs uppercase tracking-wide text-gray-400">{label}</span>
      <div className="mt-1">{children}</div>
    </label>
  );
}

function CheckboxLabel({
  label,
  checked,
  onChange,
}: {
  label: string;
  checked: boolean;
  onChange: (v: boolean) => void;
}) {
  return (
    <label className="inline-flex items-center gap-2 text-sm text-gray-200 cursor-pointer">
      <input
        type="checkbox"
        checked={checked}
        onChange={(e) => onChange(e.target.checked)}
        className="accent-indigo-500 w-4 h-4"
      />
      {label}
    </label>
  );
}
