import { useMemo } from 'react';
import { CaptureControls } from '../components/ui/CaptureControls.tsx';
import { MeasurementList } from '../components/ui/MeasurementList.tsx';
import { PolarPlot } from '../components/visualization/PolarPlot.tsx';
import { useSessionStore } from '../stores/sessionStore.ts';
import { useDeviceStore } from '../stores/deviceStore.ts';
import { computeAllSpl } from '../audio/spl.ts';
import { useNavigate } from 'react-router-dom';

export function CapturePage() {
  const measurements = useSessionStore((s) => s.measurements);
  const assignments = useDeviceStore((s) => s.assignments);
  const assignedCount = assignments.filter((a) => a.deviceId !== '').length;
  const navigate = useNavigate();

  const splData = useMemo(() => computeAllSpl(measurements), [measurements]);

  if (assignedCount === 0) {
    return (
      <div className="max-w-2xl mx-auto text-center py-12 space-y-4">
        <p className="text-gray-400">No microphones assigned yet.</p>
        <button
          onClick={() => navigate('/setup')}
          className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 text-sm"
        >
          Go to Setup
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold text-white">Capture</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="space-y-6">
          <div className="p-4 bg-gray-800 rounded-lg border border-gray-700">
            <CaptureControls />
          </div>
          <MeasurementList />
        </div>

        <div className="p-4 bg-gray-800 rounded-lg border border-gray-700">
          <h2 className="text-sm font-medium text-gray-300 mb-3">Live Preview</h2>
          <PolarPlot data={splData} size={380} />
        </div>
      </div>
    </div>
  );
}
