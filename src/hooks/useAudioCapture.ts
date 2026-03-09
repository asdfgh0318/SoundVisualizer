import { useCallback } from 'react';
import { useDeviceStore } from '../stores/deviceStore.ts';
import { useSessionStore } from '../stores/sessionStore.ts';
import { captureAllMics } from '../audio/captureEngine.ts';
import type { Measurement } from '../types/index.ts';

export function useAudioCapture() {
  const assignments = useDeviceStore((s) => s.assignments);
  const {
    currentAzimuth,
    captureDurationSec,
    sampleRate,
    captureStatus,
    triggerConfig,
    setCaptureStatus,
    setCaptureProgress,
    setError,
    addMeasurement,
  } = useSessionStore();

  const startCapture = useCallback(async () => {
    setCaptureStatus('requesting');
    setCaptureProgress(0);
    setError(null);

    try {
      setCaptureStatus('recording');

      const captures = await captureAllMics(
        assignments,
        captureDurationSec,
        sampleRate,
        (pct) => setCaptureProgress(pct),
        triggerConfig,
      );

      const measurement: Measurement = {
        id: crypto.randomUUID(),
        azimuthDeg: currentAzimuth,
        timestamp: Date.now(),
        captures,
      };

      addMeasurement(measurement);
      setCaptureProgress(100);
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Capture failed';
      setError(msg);
      setCaptureStatus('error');
    }
  }, [
    assignments,
    currentAzimuth,
    captureDurationSec,
    sampleRate,
    triggerConfig,
    setCaptureStatus,
    setCaptureProgress,
    setError,
    addMeasurement,
  ]);

  return {
    startCapture,
    isCapturing: captureStatus === 'requesting' || captureStatus === 'recording',
  };
}
