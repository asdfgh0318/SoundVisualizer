import { useEffect, useState } from 'react';
import { api, ApiError } from '../../api/client';
import type { MicConfig, MicPresetEntry, SetupPreset } from '../../api/types';
import { localId } from '../../lib/uuid';
import { useSetupStore } from '../../stores/setupStore';
import { Button } from '../ui/Button';

/** Convert frontend MicConfig list → preset entries (drops device index + local id). */
function micsToPresetEntries(mics: MicConfig[]): MicPresetEntry[] {
  return mics
    .filter((m) => m.serial.trim() !== '')
    .map((m) => ({
      serial: m.serial,
      elevation_deg: m.elevationDeg,
      calibration_file_id: m.calibrationFileId,
      alsa_card_id: m.alsaCardId,
    }));
}

/** Convert preset entries → fresh MicConfig list with new local ids and blank devices.
 *  Legacy presets (with `top_elevation_deg` / `bottom_elevation_deg` instead of
 *  `elevation_deg`) fold the first non-null value into the single elevation slot. */
function presetEntriesToMics(entries: MicPresetEntry[]): MicConfig[] {
  return entries.map((e) => ({
    id: localId(),
    serial: e.serial,
    // deviceIndex is resolved from alsaCardId by MicList's reconcile effect
    // once the live device list loads (the numeric index shifts per boot).
    deviceIndex: null,
    alsaCardId: e.alsa_card_id ?? null,
    elevationDeg:
      e.elevation_deg ?? e.top_elevation_deg ?? e.bottom_elevation_deg ?? null,
    calibrationFileId: e.calibration_file_id,
  }));
}

export function PresetControls() {
  const mics = useSetupStore((s) => s.mics);
  const replaceMics = useSetupStore((s) => s.replaceMics);

  const [presets, setPresets] = useState<SetupPreset[]>([]);
  const [error, setError] = useState<Error | null>(null);
  const [selectedId, setSelectedId] = useState<string>('');
  const [saving, setSaving] = useState(false);
  const [version, setVersion] = useState(0);

  useEffect(() => {
    let cancelled = false;
    api.listSetupPresets().then(
      (p) => !cancelled && setPresets(p),
      (e: Error | ApiError) => !cancelled && setError(e),
    );
    return () => { cancelled = true; };
  }, [version]);

  const selected = presets.find((p) => p.id === selectedId) ?? null;

  const onLoad = () => {
    if (!selected) return;
    if (mics.length > 0) {
      const ok = confirm(
        `Replace ${mics.length} mic${mics.length === 1 ? '' : 's'} with preset "${selected.name}" (${selected.mics.length} mic${selected.mics.length === 1 ? '' : 's'})? Any USB-device bindings you've made will be carried over by matching serial.`,
      );
      if (!ok) return;
    }
    // Carry over existing physical bindings (deviceIndex + alsaCardId) by serial,
    // so re-loading the preset doesn't make you re-identify every mic. Key on
    // digits when present (tolerates 810-8897 vs 8108897), else the raw serial
    // (labels like "a"/"b" have no digits — must NOT collapse to one key).
    const key = (s: string) => {
      const d = s.replace(/\D/g, '');
      return d || s.trim().toLowerCase();
    };
    const priorBySerial = new Map(
      mics
        .filter((m) => (m.alsaCardId || m.deviceIndex !== null) && key(m.serial))
        .map((m) => [key(m.serial), m]),
    );
    const loaded = presetEntriesToMics(selected.mics).map((m) => {
      const prior = key(m.serial) ? priorBySerial.get(key(m.serial)) : undefined;
      return prior
        ? { ...m, deviceIndex: prior.deviceIndex, alsaCardId: prior.alsaCardId }
        : m;
    });
    replaceMics(loaded);
  };

  const onSave = async () => {
    const portable = micsToPresetEntries(mics);
    if (portable.length === 0) {
      alert('Add at least one mic with a serial before saving a preset.');
      return;
    }
    const name = prompt('Preset name:', `${portable.length}-mic preset`)?.trim();
    if (!name) return;
    setSaving(true);
    setError(null);
    try {
      // Upsert by name: if a preset with this name exists, replace it (avoids
      // confusing duplicates with the same name).
      const existing = presets.find((p) => p.name === name);
      if (existing) {
        const ok = confirm(`Preset "${name}" already exists — overwrite it with the current ${portable.length} mics (including device bindings)?`);
        if (!ok) { setSaving(false); return; }
        await api.deleteSetupPreset(existing.id);
      }
      await api.createSetupPreset(name, portable);
      setVersion((v) => v + 1);
    } catch (e) {
      setError(e as Error);
    } finally {
      setSaving(false);
    }
  };

  const onDelete = async () => {
    if (!selected) return;
    if (!confirm(`Delete preset "${selected.name}"?`)) return;
    try {
      await api.deleteSetupPreset(selected.id);
      setSelectedId('');
      setVersion((v) => v + 1);
    } catch (e) {
      setError(e as Error);
    }
  };

  return (
    <div className="flex flex-wrap items-center gap-2 pb-3 border-b border-gray-700/60 mb-3">
      <span className="text-xs uppercase tracking-wide text-gray-500 mr-1">Presets</span>
      <select
        className="input"
        value={selectedId}
        onChange={(e) => setSelectedId(e.target.value)}
      >
        <option value="">{presets.length === 0 ? 'no saved presets' : '— pick a preset —'}</option>
        {presets.map((p) => (
          <option key={p.id} value={p.id}>
            {p.name} · {p.mics.length} mic{p.mics.length === 1 ? '' : 's'}
          </option>
        ))}
      </select>
      <Button variant="secondary" onClick={onLoad} disabled={!selected}>
        Load
      </Button>
      <Button variant="ghost" onClick={onDelete} disabled={!selected}>
        Delete
      </Button>
      <span className="grow" />
      <Button onClick={onSave} disabled={saving || mics.length === 0}>
        {saving ? 'Saving…' : '+ Save current as preset'}
      </Button>
      {error && (
        <span className="text-xs text-red-400 basis-full">Error: {error.message}</span>
      )}
    </div>
  );
}
