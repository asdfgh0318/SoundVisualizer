import { useEffect } from 'react';
import { useDeviceStore } from '../stores/deviceStore.ts';

/**
 * Hook that enumerates audio devices on mount and listens for device changes.
 */
export function useAudioDevices() {
  const enumerateDevices = useDeviceStore((s) => s.enumerateDevices);

  useEffect(() => {
    const handleChange = () => {
      enumerateDevices();
    };

    navigator.mediaDevices.addEventListener('devicechange', handleChange);
    return () => {
      navigator.mediaDevices.removeEventListener('devicechange', handleChange);
    };
  }, [enumerateDevices]);
}
