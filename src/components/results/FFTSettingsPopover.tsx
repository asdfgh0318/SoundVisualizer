import type { FFTSettings } from '../../api/types';
import { FFT_OVERLAP_OPTIONS, FFT_SIZE_OPTIONS } from '../../api/types';

interface Props {
  settings: FFTSettings;
  onChange: (s: FFTSettings) => void;
}

export function FFTSettingsBar({ settings, onChange }: Props) {
  return (
    <div className="flex items-center gap-4 px-4 py-2 bg-gray-900/40 border border-gray-700 rounded-md text-sm">
      <span className="text-xs uppercase tracking-wide text-gray-500">FFT</span>
      <label className="flex items-center gap-2">
        <span className="text-gray-400 text-xs">Size</span>
        <select
          className="input"
          value={settings.size}
          onChange={(e) => onChange({ ...settings, size: Number(e.target.value) })}
        >
          {FFT_SIZE_OPTIONS.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
      </label>
      <label className="flex items-center gap-2">
        <span className="text-gray-400 text-xs">Overlap</span>
        <select
          className="input"
          value={settings.overlap}
          onChange={(e) => onChange({ ...settings, overlap: Number(e.target.value) })}
        >
          {FFT_OVERLAP_OPTIONS.map((o) => (
            <option key={o} value={o}>
              {(o * 100).toFixed(0)}%
            </option>
          ))}
        </select>
      </label>
      <span className="text-xs text-gray-500">window: hann (Welch PSD)</span>
    </div>
  );
}
