import { useDeviceStore } from '../../stores/deviceStore.ts';
import { formatElevation } from '../../utils/angles.ts';
import { ELEVATION_ANGLES } from '../../types/index.ts';
import { LiveMeter } from './LiveMeter.tsx';

export function DeviceAssignment() {
  const { devices, assignments, permissionGranted, error, enumerateDevices, assignDevice, autoAssign, reset } =
    useDeviceStore();

  return (
    <div className="space-y-6">
      <div className="flex gap-3">
        <button
          onClick={enumerateDevices}
          className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition-colors text-sm font-medium"
        >
          {permissionGranted ? 'Refresh Devices' : 'Detect Microphones'}
        </button>
        {permissionGranted && devices.length > 0 && (
          <>
            <button
              onClick={autoAssign}
              className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-500 transition-colors text-sm font-medium"
            >
              Auto-assign UMIK
            </button>
            <button
              onClick={reset}
              className="px-4 py-2 bg-gray-700 text-gray-300 rounded-md hover:bg-gray-600 transition-colors text-sm font-medium"
            >
              Reset
            </button>
          </>
        )}
      </div>

      {error && (
        <div className="p-3 bg-red-900/50 border border-red-700 rounded-md text-red-300 text-sm">
          {error}
        </div>
      )}

      {permissionGranted && (
        <div className="text-sm text-gray-400">
          Found {devices.length} audio input{devices.length !== 1 ? 's' : ''}
        </div>
      )}

      <div className="space-y-3">
        {ELEVATION_ANGLES.map((elev) => {
          const assignment = assignments.find((a) => a.elevationDeg === elev);
          return (
            <div
              key={elev}
              className="p-3 bg-gray-800 rounded-lg border border-gray-700 space-y-2"
            >
              <div className="flex items-center gap-4">
                <span className="w-16 text-right font-mono text-sm text-gray-300 shrink-0">
                  {formatElevation(elev)}
                </span>

                <select
                  value={assignment?.deviceId || ''}
                  onChange={(e) => {
                    const dev = devices.find((d) => d.deviceId === e.target.value);
                    if (dev) {
                      assignDevice(elev, dev.deviceId, dev.label);
                    } else {
                      assignDevice(elev, '', '');
                    }
                  }}
                  className="flex-1 bg-gray-700 text-gray-200 border border-gray-600 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  aria-label={`Microphone for elevation ${formatElevation(elev)}`}
                >
                  <option value="">-- Select microphone --</option>
                  {devices.map((d) => (
                    <option key={d.deviceId} value={d.deviceId}>
                      {d.label || `Device ${d.deviceId.slice(0, 8)}...`}
                    </option>
                  ))}
                </select>

                <div
                  className={`w-3 h-3 rounded-full shrink-0 ${
                    assignment?.deviceId ? 'bg-green-500' : 'bg-gray-600'
                  }`}
                  title={assignment?.deviceId ? 'Assigned' : 'Not assigned'}
                />
              </div>

              {assignment?.deviceId && (
                <div className="ml-20">
                  <LiveMeter deviceId={assignment.deviceId} />
                </div>
              )}
            </div>
          );
        })}
      </div>

      {permissionGranted && (
        <div className="text-xs text-gray-500">
          Assign each UMIK-2 microphone to its elevation angle. Use Auto-assign to
          automatically detect UMIK/miniDSP devices.
        </div>
      )}
    </div>
  );
}
