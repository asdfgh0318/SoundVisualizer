import type { MicConfig } from '../../api/types';
import { Button } from '../ui/Button';
import { Modal } from './Modal';

interface Props {
  mics: MicConfig[];
  onCancel: () => void;
  onConfirm: () => void;
}

export function ReconfigureModal({ mics, onCancel, onConfirm }: Props) {
  return (
    <Modal
      title="Top half done — reconfigure mics for bottom"
      footer={
        <>
          <Button variant="ghost" onClick={onCancel}>
            Skip bottom
          </Button>
          <Button onClick={onConfirm}>Mics moved — start bottom →</Button>
        </>
      }
    >
      <p>
        Move each mic from its <strong>top</strong> position to its <strong>bottom</strong>{' '}
        position, then click confirm.
      </p>
      <table className="w-full text-xs mt-2">
        <thead>
          <tr className="text-left text-gray-500 border-b border-gray-700">
            <th className="py-1.5 pr-3 font-medium">Mic</th>
            <th className="pr-3 font-medium">Top</th>
            <th className="pr-3 font-medium">Bottom</th>
          </tr>
        </thead>
        <tbody>
          {mics.map((m) => (
            <tr key={m.id} className="border-b border-gray-700/50 last:border-b-0">
              <td className="py-1.5 pr-3 font-mono text-gray-200">{m.serial}</td>
              <td className="pr-3 text-gray-400">{m.topElevationDeg ?? '—'}°</td>
              <td className="pr-3 text-indigo-300">{m.bottomElevationDeg ?? '—'}°</td>
            </tr>
          ))}
        </tbody>
      </table>
    </Modal>
  );
}
