import { Button } from '../ui/Button';
import { Modal } from './Modal';

interface Props {
  cutoffsConfigured: boolean;
  fakeMode: boolean;
  onCancel: () => void;
  onConfirm: () => void;
}

export function SafetyModal({ cutoffsConfigured, fakeMode, onCancel, onConfirm }: Props) {
  if (fakeMode) {
    return (
      <Modal
        title="✦ Fake capture (no hardware)"
        footer={
          <>
            <Button variant="ghost" onClick={onCancel}>Cancel</Button>
            <Button onClick={onConfirm}>Start fake capture</Button>
          </>
        }
      >
        <p>
          This skips the Tyto motor and the UMIK-2 inputs entirely. Synthetic drone-noise WAVs
          and telemetry CSV will be generated for every PWM step, then the wizard plays out a
          simulated progress animation so you can exercise the flow end-to-end.
        </p>
        <p className="text-gray-400 text-xs">
          Use this to test the wizard UX, develop the Results tabs against realistic data, or
          demo the app without the rig.
        </p>
      </Modal>
    );
  }
  return (
    <Modal
      title="⚠ Propeller will spin"
      footer={
        <>
          <Button variant="ghost" onClick={onCancel}>Cancel</Button>
          <Button variant="danger" onClick={onConfirm}>I understand — start capture</Button>
        </>
      }
    >
      <p>The Tyto stand will drive the motor through the configured PWM ramp. Make sure:</p>
      <ul className="list-disc pl-5 space-y-1 text-gray-300">
        <li>The test rig is mechanically secure and clamped down.</li>
        <li>No loose objects, hands, or persons are within prop sweep distance.</li>
        <li>Eye protection is on.</li>
        <li>All mics are mounted at their configured elevation positions.</li>
      </ul>
      {!cutoffsConfigured && (
        <div className="mt-2 p-3 rounded-md border border-amber-700/60 bg-amber-900/20 text-amber-300 text-xs">
          ⚠ No safety cutoffs are enabled. The watchdog will <em>not</em> auto-stop the motor.
          Consider going back and enabling them in Setup.
        </div>
      )}
    </Modal>
  );
}
