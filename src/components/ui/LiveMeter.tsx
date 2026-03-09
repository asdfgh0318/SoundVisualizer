import { useEffect, useRef, useState } from 'react';

interface LiveMeterProps {
  deviceId: string;
}

/**
 * Real-time audio level meter for a single microphone.
 * Uses AnalyserNode to show live RMS level — tap the mic membrane to identify it.
 */
export function LiveMeter({ deviceId }: LiveMeterProps) {
  const [level, setLevel] = useState(-Infinity);
  const [peak, setPeak] = useState(-Infinity);
  const [error, setError] = useState<string | null>(null);
  const cleanupRef = useRef<(() => void) | null>(null);

  useEffect(() => {
    if (!deviceId) return;

    let cancelled = false;

    async function start() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          audio: {
            deviceId: { exact: deviceId },
            echoCancellation: false,
            noiseSuppression: false,
            autoGainControl: false,
          },
        });

        if (cancelled) {
          stream.getTracks().forEach((t) => t.stop());
          return;
        }

        const ctx = new AudioContext();
        const source = ctx.createMediaStreamSource(stream);
        const analyser = ctx.createAnalyser();
        analyser.fftSize = 2048;
        analyser.smoothingTimeConstant = 0.3;
        source.connect(analyser);

        const buffer = new Float32Array(analyser.fftSize);
        let peakHold = -Infinity;
        let peakDecay = 0;

        const tick = () => {
          if (cancelled) return;

          analyser.getFloatTimeDomainData(buffer);

          // Compute RMS
          let sum = 0;
          for (let i = 0; i < buffer.length; i++) {
            sum += buffer[i] * buffer[i];
          }
          const rms = Math.sqrt(sum / buffer.length);
          const db = rms > 0 ? 20 * Math.log10(rms) : -Infinity;

          // Peak hold with decay
          if (db > peakHold) {
            peakHold = db;
            peakDecay = 0;
          } else {
            peakDecay++;
            if (peakDecay > 30) { // ~0.5s at 60fps
              peakHold = Math.max(db, peakHold - 0.5);
            }
          }

          setLevel(db);
          setPeak(peakHold);
          requestAnimationFrame(tick);
        };

        requestAnimationFrame(tick);

        cleanupRef.current = () => {
          cancelled = true;
          source.disconnect();
          stream.getTracks().forEach((t) => t.stop());
          ctx.close();
        };
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : 'Failed to open mic');
        }
      }
    }

    start();

    return () => {
      cancelled = true;
      cleanupRef.current?.();
      cleanupRef.current = null;
    };
  }, [deviceId]);

  if (!deviceId) return null;

  if (error) {
    return <div className="text-xs text-red-400">{error}</div>;
  }

  // Map dB to bar width: -60 dB = 0%, 0 dB = 100%
  const minDb = -60;
  const maxDb = 0;
  const pct = Math.max(0, Math.min(100, ((level - minDb) / (maxDb - minDb)) * 100));
  const peakPct = Math.max(0, Math.min(100, ((peak - minDb) / (maxDb - minDb)) * 100));

  // Color: green below -20, yellow -20 to -6, red above -6
  const barColor = level > -6 ? 'bg-red-500' : level > -20 ? 'bg-yellow-500' : 'bg-green-500';

  return (
    <div className="space-y-1">
      <div className="flex items-center gap-2">
        <div className="relative flex-1 h-4 bg-gray-900 rounded overflow-hidden">
          {/* Level bar */}
          <div
            className={`absolute inset-y-0 left-0 ${barColor} transition-[width] duration-75`}
            style={{ width: `${pct}%` }}
          />
          {/* Peak indicator */}
          {isFinite(peak) && (
            <div
              className="absolute inset-y-0 w-0.5 bg-white"
              style={{ left: `${peakPct}%` }}
            />
          )}
          {/* Scale marks */}
          {[-48, -36, -24, -12, -6, 0].map((db) => {
            const x = ((db - minDb) / (maxDb - minDb)) * 100;
            return (
              <div
                key={db}
                className="absolute top-0 h-full w-px bg-gray-700"
                style={{ left: `${x}%` }}
              />
            );
          })}
        </div>
        <span className="w-16 text-right font-mono text-xs text-gray-400 shrink-0">
          {isFinite(level) ? `${level.toFixed(1)}` : '--'} dB
        </span>
      </div>
    </div>
  );
}
