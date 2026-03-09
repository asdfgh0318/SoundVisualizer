import { useSessionStore } from '../../stores/sessionStore.ts';
import { useWavExport } from '../../hooks/useWavExport.ts';
import { formatAzimuth, formatElevation } from '../../utils/angles.ts';
import { captureSplDb } from '../../audio/spl.ts';

export function MeasurementList() {
  const measurements = useSessionStore((s) => s.measurements);
  const deleteMeasurement = useSessionStore((s) => s.deleteMeasurement);
  const { exportMeasurement } = useWavExport();

  if (measurements.length === 0) {
    return (
      <div className="text-center text-gray-500 py-8 text-sm">
        No measurements yet. Capture your first position above.
      </div>
    );
  }

  return (
    <div className="space-y-2">
      <h3 className="text-sm font-medium text-gray-300">
        Measurements ({measurements.length})
      </h3>
      <div className="overflow-x-auto">
        <table className="w-full text-sm text-left">
          <thead className="text-xs text-gray-400 border-b border-gray-700">
            <tr>
              <th className="py-2 px-3">Azimuth</th>
              {measurements[0]?.captures.map((c) => (
                <th key={c.elevationDeg} className="py-2 px-3">
                  {formatElevation(c.elevationDeg)}
                </th>
              ))}
              <th className="py-2 px-3 text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            {measurements.map((m) => (
              <tr key={m.id} className="border-b border-gray-800 hover:bg-gray-800/50">
                <td className="py-2 px-3 font-mono text-gray-200">
                  {formatAzimuth(m.azimuthDeg)}
                </td>
                {m.captures.map((c) => {
                  const spl = captureSplDb(c);
                  return (
                    <td key={c.elevationDeg} className="py-2 px-3 font-mono text-gray-400">
                      {isFinite(spl) ? `${spl.toFixed(1)} dB` : '--'}
                    </td>
                  );
                })}
                <td className="py-2 px-3 text-right">
                  <button
                    onClick={() => exportMeasurement(m)}
                    className="text-indigo-400 hover:text-indigo-300 text-xs mr-3"
                  >
                    WAV
                  </button>
                  <button
                    onClick={() => deleteMeasurement(m.id)}
                    className="text-red-400 hover:text-red-300 text-xs"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
