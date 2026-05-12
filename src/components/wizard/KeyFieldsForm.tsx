import type { WizardForm } from '../../stores/wizardStore';

interface Props {
  form: WizardForm;
  onChange: (patch: Partial<WizardForm>) => void;
}

export function KeyFieldsForm({ form, onChange }: Props) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <Field label="Motor" required>
        <input
          className="input w-full"
          placeholder="e.g. T-Motor F60 Pro IV"
          value={form.motor}
          onChange={(e) => onChange({ motor: e.target.value })}
        />
      </Field>
      <Field label="Propeller" required>
        <input
          className="input w-full"
          placeholder="e.g. HQProp 5x4.3x3"
          value={form.propeller}
          onChange={(e) => onChange({ propeller: e.target.value })}
        />
      </Field>
      <Field label="Shroud">
        <input
          className="input w-full"
          placeholder="e.g. none / 5-inch duct"
          value={form.shroud}
          onChange={(e) => onChange({ shroud: e.target.value })}
        />
      </Field>
      <Field label="Notes">
        <input
          className="input w-full"
          placeholder="any free-form qualifier"
          value={form.notes}
          onChange={(e) => onChange({ notes: e.target.value })}
        />
      </Field>
    </div>
  );
}

function Field({
  label,
  required,
  children,
}: {
  label: string;
  required?: boolean;
  children: React.ReactNode;
}) {
  return (
    <label className="block">
      <span className="text-xs uppercase tracking-wide text-gray-400">
        {label}
        {required && <span className="text-amber-400 ml-1">*</span>}
      </span>
      <div className="mt-1">{children}</div>
    </label>
  );
}
