import { AudioDeviceList } from '../components/setup/AudioDeviceList';
import { CalibrationLibrary } from '../components/setup/CalibrationLibrary';
import { CutoffsConfig } from '../components/setup/CutoffsConfig';
import { DeferredCard } from '../components/setup/DeferredCard';
import { MicList } from '../components/setup/MicList';
import { TytoStatus } from '../components/setup/TytoStatus';
import { Card } from '../components/ui/Card';

export function SetupPage() {
  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <header>
        <h1 className="text-2xl font-bold text-white">Setup</h1>
        <p className="text-sm text-gray-400 mt-1">
          Configure microphones, calibration files, and Tyto safety cutoffs before starting captures.
        </p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <Card
            title="Audio devices"
            description="Read-only — pick the index when assigning a USB device to a microphone below."
          >
            <AudioDeviceList />
          </Card>
        </div>
        <Card title="Tyto stand" description="Live connection state.">
          <TytoStatus />
        </Card>
      </div>

      <Card
        title="Microphones"
        description="Manual placement — one row per UMIK-2. Top and bottom elevations are independent; the user manually re-mounts mics between captures."
      >
        <MicList />
      </Card>

      <Card
        title="UMIK-2 calibration files"
        description="Upload one .txt per mic. Stored on the server keyed by serial."
      >
        <CalibrationLibrary />
      </Card>

      <Card
        title="Safety cutoffs (Tyto Robotics 1585)"
        description="Watchdog reads telemetry at ~33 Hz and slams PWM to 1000 µs on the first tripped channel. Trip is latched until manually reset."
      >
        <CutoffsConfig />
      </Card>

      <DeferredCard
        title="Norsonic NOR-145"
        reason="Pending hardware delivery. Will integrate as an additional acoustic source in a later phase."
      />
    </div>
  );
}
