import { useState } from 'react';
import { useSessionStore } from '../../stores/sessionStore.ts';
import { useWavExport } from '../../hooks/useWavExport.ts';

export function ExportPanel() {
  const measurements = useSessionStore((s) => s.measurements);
  const { exportAll } = useWavExport();
  const [bitDepth, setBitDepth] = useState<16 | 32>(16);

  if (measurements.length === 0) return null;

  return (
    <div className="p-4 bg-gray-800 rounded-lg border border-gray-700 space-y-3">
      <h3 className="text-sm font-medium text-gray-300">Export</h3>

      <div className="flex items-center gap-4">
        <label className="text-sm text-gray-400">
          <input
            type="radio"
            name="bitDepth"
            value={16}
            checked={bitDepth === 16}
            onChange={() => setBitDepth(16)}
            className="mr-1"
          />
          16-bit PCM
        </label>
        <label className="text-sm text-gray-400">
          <input
            type="radio"
            name="bitDepth"
            value={32}
            checked={bitDepth === 32}
            onChange={() => setBitDepth(32)}
            className="mr-1"
          />
          32-bit Float
        </label>
      </div>

      <button
        onClick={() => exportAll(bitDepth)}
        className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 text-sm font-medium"
      >
        Download All ({measurements.length * (measurements[0]?.captures.length ?? 0)} WAV
        files)
      </button>

      <p className="text-xs text-gray-500">
        Files named: session_az[angle]_el[angle].wav
      </p>
    </div>
  );
}
