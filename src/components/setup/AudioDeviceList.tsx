import { useEffect, useState } from 'react';
import { api, ApiError } from '../../api/client';
import type { AudioDeviceInfo } from '../../api/types';
import { Empty, ErrorMessage, Loading } from '../ui/Status';

export function AudioDeviceList() {
  const [devices, setDevices] = useState<AudioDeviceInfo[] | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [reload, setReload] = useState(0);

  useEffect(() => {
    let cancelled = false;
    setDevices(null);
    setError(null);
    api.listAudioDevices().then(
      (d) => !cancelled && setDevices(d),
      (e: Error | ApiError) => !cancelled && setError(e),
    );
    return () => { cancelled = true; };
  }, [reload]);

  if (error) return <ErrorMessage error={error} onRetry={() => setReload((r) => r + 1)} />;
  if (!devices) return <Loading />;
  if (devices.length === 0) return <Empty>No input devices detected.</Empty>;

  return (
    <table className="w-full text-sm">
      <thead>
        <tr className="text-left text-gray-400 border-b border-gray-700">
          <th className="py-2 pr-4 font-medium">#</th>
          <th className="pr-4 font-medium">Name</th>
          <th className="pr-4 font-medium">Host API</th>
          <th className="font-medium">Channels</th>
        </tr>
      </thead>
      <tbody>
        {devices.map((d) => (
          <tr key={d.index} className="border-b border-gray-700/50 last:border-b-0">
            <td className="py-1.5 pr-4 font-mono text-gray-300">{d.index}</td>
            <td className="pr-4 text-gray-200">{d.name}</td>
            <td className="pr-4 text-gray-400">{d.hostapi}</td>
            <td className="text-gray-400">{d.max_input_channels}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
