import { useEffect } from 'react';
import { useSetupStore } from '../../stores/setupStore';
import { useWizardStore } from '../../stores/wizardStore';
import { Button } from '../ui/Button';
import { Card } from '../ui/Card';
import { InfoToggle } from '../ui/InfoToggle';
import { CAPTURE_HELP } from '../../content/parameterHelp';
import { KeyFieldsForm } from './KeyFieldsForm';
import { ResearchTreeNodePicker } from './ResearchTreeNodePicker';
import { MicSelector } from './MicSelector';
import { PWMRampEditor } from './PWMRampEditor';

export function WizardForm() {
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

  // A capture requires fully-configured mics (USB device + serial).
  const canContinue = baseFilled && usableMics.length > 0;


  return (
    <div className="space-y-6">
      <Card title="Test article" description="Becomes the base motor__propeller__shroud__notes that groups the measurements on the Results page. Optionally link to a research-tree node to autofill fields and push the Results URL back on success.">
        <div className="space-y-4">
          <ResearchTreeNodePicker form={form} onChange={updateForm} />
          <KeyFieldsForm form={form} onChange={updateForm} />
        </div>
      </Card>

      <Card title="ESC signal ramp" description="One acoustic + one performance measurement saved per step.">
        <PWMRampEditor
          steps={form.pwm_steps}
          onChange={(s) => updateForm({ pwm_steps: s })}
        />
      </Card>

      <Card title="Capture settings">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <Labeled label="Sample rate (Hz)" info={CAPTURE_HELP.sample_rate}>
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
          per step is configured in the ESC signal ramp above.
        </p>
      </Card>

      <Card title="Microphones" description="Pick which configured mics to record in this capture.">
        <MicSelector
          mics={mics}
          selectedIds={form.selected_mic_ids}
          onChange={(ids) => updateForm({ selected_mic_ids: ids })}
        />
      </Card>

      <Card title="Advanced">
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <Labeled label="Stabilize window (samples)" info={CAPTURE_HELP.stabilize_window}>
            <input
              type="number"
              min={1}
              className="input w-full"
              value={form.stabilize_window}
              onChange={(e) => updateForm({ stabilize_window: Number(e.target.value) })}
            />
          </Labeled>
          <Labeled label="Stabilize tolerance (RPM)" info={CAPTURE_HELP.stabilize_tolerance}>
            <input
              type="number"
              min={0.1}
              step={0.1}
              className="input w-full"
              value={form.stabilize_tolerance}
              onChange={(e) => updateForm({ stabilize_tolerance: Number(e.target.value) })}
            />
          </Labeled>
          <Labeled label="Stabilize timeout (s)" info={CAPTURE_HELP.stabilize_timeout}>
            <input
              type="number"
              min={1}
              className="input w-full"
              value={form.stabilize_timeout_seconds}
              onChange={(e) => updateForm({ stabilize_timeout_seconds: Number(e.target.value) })}
            />
          </Labeled>
          <Labeled label="Trigger sync" info={CAPTURE_HELP.trigger_sync}>
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

      <div className="flex items-center justify-end gap-3 pt-2 border-t border-gray-700">
        <Button onClick={() => setPhase('review')} disabled={!canContinue}>
          Continue → Review
        </Button>
      </div>
      {!canContinue && baseFilled && (
        <p className="text-xs text-gray-500 -mt-2">
          To start a capture, configure at least one mic with a USB device on the Setup page.
        </p>
      )}
    </div>
  );
}

function Labeled({ label, info, children }: { label: string; info?: string; children: React.ReactNode }) {
  return (
    <div className="block">
      <span className="text-xs uppercase tracking-wide text-gray-400">
        {label}
        {info && <InfoToggle label={label}>{info}</InfoToggle>}
      </span>
      <div className="mt-1">{children}</div>
    </div>
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
