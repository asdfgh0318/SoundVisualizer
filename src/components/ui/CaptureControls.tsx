import { useSessionStore } from '../../stores/sessionStore.ts';
import { useAudioCapture } from '../../hooks/useAudioCapture.ts';
import { formatAzimuth } from '../../utils/angles.ts';

export function CaptureControls() {
  const {
    currentAzimuth,
    setCurrentAzimuth,
    captureDurationSec,
    setCaptureDuration,
    captureStatus,
    captureProgress,
    errorMessage,
    suggestNextAzimuth,
    triggerConfig,
    setTriggerConfig,
  } = useSessionStore();

  const { startCapture, isCapturing } = useAudioCapture();

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label
            htmlFor="azimuth"
            className="block text-sm font-medium text-gray-300 mb-1"
          >
            Azimuth angle
          </label>
          <div className="flex gap-2">
            <input
              id="azimuth"
              type="number"
              min={0}
              max={359}
              step={1}
              value={currentAzimuth}
              onChange={(e) => setCurrentAzimuth(Number(e.target.value))}
              disabled={isCapturing}
              className="flex-1 bg-gray-700 text-gray-200 border border-gray-600 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50"
            />
            <button
              onClick={() => setCurrentAzimuth(suggestNextAzimuth())}
              disabled={isCapturing}
              className="px-3 py-2 bg-gray-600 text-gray-300 rounded-md hover:bg-gray-500 text-xs disabled:opacity-50"
              title="Suggest next uncaptured azimuth angle"
            >
              Next
            </button>
          </div>
        </div>

        <div>
          <label
            htmlFor="duration"
            className="block text-sm font-medium text-gray-300 mb-1"
          >
            Duration (seconds)
          </label>
          <input
            id="duration"
            type="number"
            min={0.5}
            max={30}
            step={0.5}
            value={captureDurationSec}
            onChange={(e) => setCaptureDuration(Number(e.target.value))}
            disabled={isCapturing}
            className="w-full bg-gray-700 text-gray-200 border border-gray-600 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50"
          />
        </div>
      </div>

      {/* Trigger sync controls */}
      <div className="p-3 bg-gray-800 rounded-md border border-gray-700 space-y-2">
        <label className="flex items-center gap-2 text-sm text-gray-300 cursor-pointer">
          <input
            type="checkbox"
            checked={triggerConfig.enabled}
            onChange={(e) => setTriggerConfig({ enabled: e.target.checked })}
            disabled={isCapturing}
            className="rounded border-gray-600 bg-gray-700 text-indigo-500 focus:ring-indigo-500"
          />
          Trigger sync (align mics on sound onset)
        </label>
        {triggerConfig.enabled && (
          <div className="grid grid-cols-2 gap-2">
            <div>
              <label
                htmlFor="trigger-threshold"
                className="block text-xs text-gray-500 mb-0.5"
              >
                Threshold (dBFS)
              </label>
              <input
                id="trigger-threshold"
                type="number"
                min={-96}
                max={0}
                step={1}
                value={triggerConfig.thresholdDb}
                onChange={(e) =>
                  setTriggerConfig({ thresholdDb: Number(e.target.value) })
                }
                disabled={isCapturing}
                className="w-full bg-gray-700 text-gray-200 border border-gray-600 rounded px-2 py-1 text-xs focus:outline-none focus:ring-1 focus:ring-indigo-500 disabled:opacity-50"
              />
            </div>
            <div>
              <label
                htmlFor="trigger-preroll"
                className="block text-xs text-gray-500 mb-0.5"
              >
                Pre-roll (ms)
              </label>
              <input
                id="trigger-preroll"
                type="number"
                min={0}
                max={100}
                step={1}
                value={Math.round((triggerConfig.prerollSamples / 48000) * 1000)}
                onChange={(e) =>
                  setTriggerConfig({
                    prerollSamples: Math.round((Number(e.target.value) / 1000) * 48000),
                  })
                }
                disabled={isCapturing}
                className="w-full bg-gray-700 text-gray-200 border border-gray-600 rounded px-2 py-1 text-xs focus:outline-none focus:ring-1 focus:ring-indigo-500 disabled:opacity-50"
              />
            </div>
          </div>
        )}
      </div>

      <button
        onClick={startCapture}
        disabled={isCapturing}
        className={`w-full py-3 rounded-md font-medium text-sm transition-colors ${
          isCapturing
            ? 'bg-red-600 text-white cursor-wait'
            : 'bg-green-600 text-white hover:bg-green-700'
        }`}
      >
        {isCapturing
          ? `Recording at ${formatAzimuth(currentAzimuth)}... ${captureProgress}%`
          : `Capture at ${formatAzimuth(currentAzimuth)}`}
      </button>

      {captureStatus === 'done' && (
        <div className="text-sm text-green-400">Capture complete.</div>
      )}

      {captureStatus === 'error' && errorMessage && (
        <div className="p-3 bg-red-900/50 border border-red-700 rounded-md text-red-300 text-sm">
          {errorMessage}
        </div>
      )}
    </div>
  );
}
