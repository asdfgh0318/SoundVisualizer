import { useCallback } from 'react';
import { useSessionStore } from '../stores/sessionStore.ts';
import { downloadCapture } from '../audio/wavEncoder.ts';
import type { Measurement } from '../types/index.ts';

export function useWavExport() {
  const measurements = useSessionStore((s) => s.measurements);
  const sessionName = useSessionStore((s) => s.sessionName);

  const exportMeasurement = useCallback(
    (measurement: Measurement, bitDepth: 16 | 32 = 16) => {
      const prefix = sessionName || 'capture';
      for (const capture of measurement.captures) {
        const filename = `${prefix}_az${measurement.azimuthDeg}_el${capture.elevationDeg}.wav`;
        downloadCapture(capture.audioData, capture.sampleRate, filename, bitDepth);
      }
    },
    [sessionName],
  );

  const exportAll = useCallback(
    (bitDepth: 16 | 32 = 16) => {
      for (const m of measurements) {
        exportMeasurement(m, bitDepth);
      }
    },
    [measurements, exportMeasurement],
  );

  return { exportMeasurement, exportAll };
}
