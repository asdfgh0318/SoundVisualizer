import { useEffect, useRef, useState } from 'react';
import { api, ApiError } from '../../api/client';
import type { CalibrationSummary } from '../../api/types';
import { useSetupStore } from '../../stores/setupStore';
import { Empty, ErrorMessage, Loading } from '../ui/Status';

export function CalibrationLibrary() {
  const [items, setItems] = useState<CalibrationSummary[] | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState<Error | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);
  const calibrationsVersion = useSetupStore((s) => s.calibrationsVersion);
  const bump = useSetupStore((s) => s.bumpCalibrations);

  useEffect(() => {
    let cancelled = false;
    setItems(null);
    setError(null);
    api.listCalibrations().then(
      (d) => !cancelled && setItems(d),
      (e: Error | ApiError) => !cancelled && setError(e),
    );
    return () => { cancelled = true; };
  }, [calibrationsVersion]);

  const onUpload = async (file: File) => {
    setUploading(true);
    setUploadError(null);
    try {
      await api.uploadCalibration(file);
      bump();
    } catch (e) {
      setUploadError(e as Error);
    } finally {
      setUploading(false);
      if (fileRef.current) fileRef.current.value = '';
    }
  };

  return (
    <div className="space-y-4">
      {error && <ErrorMessage error={error} onRetry={bump} />}
      {!error && items === null && <Loading />}
      {items && items.length === 0 && <Empty>No calibration files uploaded.</Empty>}
      {items && items.length > 0 && (
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-gray-400 border-b border-gray-700">
              <th className="py-2 pr-4 font-medium">Serial / ID</th>
              <th className="pr-4 font-medium">Sens factor</th>
              <th className="pr-4 font-medium">AGain</th>
              <th className="pr-4 font-medium">Range</th>
              <th className="font-medium">Points</th>
            </tr>
          </thead>
          <tbody>
            {items.map((c) => (
              <tr key={c.id} className="border-b border-gray-700/50 last:border-b-0">
                <td className="py-1.5 pr-4 font-mono text-gray-200">{c.id}</td>
                <td className="pr-4 text-gray-300">{c.sens_factor_db?.toFixed(3) ?? '—'} dB</td>
                <td className="pr-4 text-gray-400">
                  {c.again_db !== null ? `${c.again_db.toFixed(1)} dB` : '—'}
                </td>
                <td className="pr-4 text-gray-400">
                  {c.freq_min_hz.toFixed(0)}–{c.freq_max_hz.toFixed(0)} Hz
                </td>
                <td className="text-gray-400">{c.n_points}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <div className="flex items-center gap-3 pt-2 border-t border-gray-700/50">
        <input
          ref={fileRef}
          type="file"
          accept=".txt,.cal"
          className="text-sm text-gray-300 file:mr-3 file:py-1.5 file:px-3 file:rounded-md file:border-0 file:bg-gray-700 file:text-gray-200 file:cursor-pointer hover:file:bg-gray-600"
          onChange={(e) => {
            const f = e.target.files?.[0];
            if (f) onUpload(f);
          }}
        />
        {uploading && <span className="text-xs text-gray-400">Uploading…</span>}
        {uploadError && (
          <span className="text-xs text-red-400">Upload failed: {uploadError.message}</span>
        )}
      </div>
      <p className="text-xs text-gray-500">
        Upload a miniDSP .txt calibration file. Serial is auto-detected from the file header.
      </p>
    </div>
  );
}
