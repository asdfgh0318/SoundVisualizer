import { Button } from '../ui/Button';
import { Modal } from './Modal';

interface Props {
  half: 'top' | 'bottom';
  cutoffsConfigured: boolean;
  onCancel: () => void;
  onConfirm: () => void;
}

export function SafetyModal({ half, cutoffsConfigured, onCancel, onConfirm }: Props) {
  return (
    <Modal
      title="⚠ Propeller will spin"
      footer={
        <>
          <Button variant="ghost" onClick={onCancel}>
            Cancel
          </Button>
          <Button variant="danger" onClick={onConfirm}>
            I understand — start {half} half
          </Button>
        </>
      }
    >
      <p>
        The Tyto stand will drive the motor through the configured PWM ramp. Make sure:
      </p>
      <ul className="list-disc pl-5 space-y-1 text-gray-300">
        <li>The test rig is mechanically secure and clamped down.</li>
        <li>No loose objects, hands, or persons are within prop sweep distance.</li>
        <li>Eye protection is on.</li>
        <li>Mics are mounted at their <strong>{half}</strong>-half positions.</li>
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
