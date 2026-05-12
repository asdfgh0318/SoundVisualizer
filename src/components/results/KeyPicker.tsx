import { useEffect, useState } from 'react';
import { api, ApiError } from '../../api/client';
import type { Key } from '../../api/types';

interface Props {
  value: string | null;
  onChange: (slug: string | null) => void;
}

export function KeyPicker({ value, onChange }: Props) {
  const [keys, setKeys] = useState<Key[] | null>(null);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    api.listKeys().then(
      (k) => {
        setKeys(k);
        if (!value && k.length > 0) onChange(k[0].slug);
      },
      (e: Error | ApiError) => setError(e),
    );
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (error)
    return <div className="text-sm text-red-400">Error loading keys: {error.message}</div>;
  if (!keys) return <div className="text-sm text-gray-400 italic">Loading…</div>;
  if (keys.length === 0)
    return <div className="text-sm text-gray-400 italic">No measurements yet — run a capture.</div>;

  return (
    <label className="block">
      <span className="text-xs uppercase tracking-wide text-gray-400 mr-3">Key</span>
      <select
        className="input min-w-[24rem]"
        value={value ?? ''}
        onChange={(e) => onChange(e.target.value || null)}
      >
        {keys.map((k) => (
          <option key={k.slug} value={k.slug}>
            {k.motor} · {k.propeller} · {k.shroud} · {k.notes}
          </option>
        ))}
      </select>
    </label>
  );
}
