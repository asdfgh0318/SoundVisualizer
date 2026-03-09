import { DeviceAssignment } from '../components/ui/DeviceAssignment.tsx';
import { useAudioDevices } from '../hooks/useAudioDevices.ts';
import { useDeviceStore } from '../stores/deviceStore.ts';
import { useNavigate } from 'react-router-dom';

export function SetupPage() {
  useAudioDevices();
  const assignments = useDeviceStore((s) => s.assignments);
  const assignedCount = assignments.filter((a) => a.deviceId !== '').length;
  const navigate = useNavigate();

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Microphone Setup</h1>
        <p className="text-sm text-gray-400 mt-1">
          Assign each UMIK-2 microphone to its elevation position in the measurement arc.
        </p>
      </div>

      <DeviceAssignment />

      <div className="flex items-center justify-between pt-4 border-t border-gray-700">
        <span className="text-sm text-gray-400">
          {assignedCount} of 5 microphones assigned
        </span>
        <button
          onClick={() => navigate('/capture')}
          disabled={assignedCount === 0}
          className="px-6 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Continue to Capture
        </button>
      </div>
    </div>
  );
}
