import type { MicConfig } from '../../api/types';

interface Props {
  mics: MicConfig[];
  selectedIds: string[];
  onChange: (ids: string[]) => void;
}

export function MicSelector({ mics, selectedIds, onChange }: Props) {
  if (mics.length === 0) {
    return (
      <p className="text-sm text-amber-400/90">
        No microphones configured. Go to <strong>Setup</strong> first and add at least one mic.
      </p>
    );
  }

  const toggle = (id: string) =>
    onChange(selectedIds.includes(id) ? selectedIds.filter((x) => x !== id) : [...selectedIds, id]);

  const allSelected = mics.every((m) => selectedIds.includes(m.id));
  const toggleAll = () => onChange(allSelected ? [] : mics.map((m) => m.id));

  return (
    <div className="space-y-2">
      <button
        type="button"
        onClick={toggleAll}
        className="text-xs text-indigo-400 hover:text-indigo-300 underline"
      >
        {allSelected ? 'Deselect all' : 'Select all'}
      </button>
      <ul className="space-y-1">
        {mics.map((m) => {
          const checked = selectedIds.includes(m.id);
          const ready = m.serial && m.deviceIndex !== null;
          return (
            <li
              key={m.id}
              className={`flex items-center gap-3 px-3 py-2 rounded-md border ${
                checked ? 'bg-gray-900/60 border-gray-700' : 'border-gray-800'
              }`}
            >
              <input
                type="checkbox"
                checked={checked}
                onChange={() => toggle(m.id)}
                disabled={!ready}
                className="accent-indigo-500 w-4 h-4"
              />
              <span className="font-mono text-sm text-gray-200">{m.serial || '(no serial)'}</span>
              <span className="text-xs text-gray-500">device #{m.deviceIndex ?? '—'}</span>
              <span className="text-xs text-gray-500 ml-auto">
                top {m.topElevationDeg ?? '—'}° · bottom {m.bottomElevationDeg ?? '—'}°
              </span>
              {!ready && (
                <span className="text-xs text-amber-400">incomplete config</span>
              )}
            </li>
          );
        })}
      </ul>
    </div>
  );
}
