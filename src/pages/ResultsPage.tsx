import { useMemo, useState } from 'react';
import { PolarPlot } from '../components/visualization/PolarPlot.tsx';
import { ContourPlot } from '../components/visualization/ContourPlot.tsx';
import { FrequencyResponsePlot } from '../components/visualization/FrequencyResponsePlot.tsx';
import { DirectivityIndexPlot } from '../components/visualization/DirectivityIndexPlot.tsx';
import { PolarAtFrequency } from '../components/visualization/PolarAtFrequency.tsx';
import { DirectivityBalloon } from '../components/visualization/DirectivityBalloon.tsx';
import { ExportPanel } from '../components/ui/ExportPanel.tsx';
import { useSessionStore } from '../stores/sessionStore.ts';
import { computeAllSpl } from '../audio/spl.ts';
import { computeAllSpectra } from '../audio/spectrum.ts';
import { computeDirectivityMetrics } from '../audio/spinorama.ts';

type Tab = 'contour' | 'polar' | 'frequency' | 'di' | 'balloon' | 'broadband';

const TABS: { id: Tab; label: string }[] = [
  { id: 'contour', label: 'Contour' },
  { id: 'frequency', label: 'Freq Response' },
  { id: 'polar', label: 'Polar @ Freq' },
  { id: 'di', label: 'SP & DI' },
  { id: 'balloon', label: '3D Balloon' },
  { id: 'broadband', label: 'Broadband' },
];

export function ResultsPage() {
  const measurements = useSessionStore((s) => s.measurements);
  const [activeTab, setActiveTab] = useState<Tab>('contour');
  const [selectedFreq, setSelectedFreq] = useState(1000);

  const splData = useMemo(() => computeAllSpl(measurements), [measurements]);
  const spectra = useMemo(() => computeAllSpectra(measurements), [measurements]);
  const metrics = useMemo(() => computeDirectivityMetrics(splData), [splData]);

  return (
    <div className="max-w-6xl mx-auto space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-white">Results</h1>
        {measurements.length > 0 && (
          <div className="flex items-center gap-4 text-sm text-gray-400">
            <span>{measurements.length} positions</span>
            <span>{splData.length} data points</span>
          </div>
        )}
      </div>

      {/* Tab bar */}
      <div className="flex gap-1 border-b border-gray-700 overflow-x-auto">
        {TABS.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2 text-sm font-medium whitespace-nowrap transition-colors ${
              activeTab === tab.id
                ? 'text-indigo-400 border-b-2 border-indigo-400'
                : 'text-gray-400 hover:text-gray-200'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Frequency selector for frequency-dependent views */}
      {(activeTab === 'polar' || activeTab === 'balloon') && (
        <div className="flex items-center gap-3 p-3 bg-gray-800 rounded-lg border border-gray-700">
          <label htmlFor="freq-select" className="text-sm text-gray-300">
            Frequency:
          </label>
          <input
            id="freq-select"
            type="range"
            min={20}
            max={20000}
            step={1}
            value={selectedFreq}
            onChange={(e) => setSelectedFreq(Number(e.target.value))}
            className="flex-1"
          />
          <input
            type="number"
            min={20}
            max={20000}
            value={selectedFreq}
            onChange={(e) => setSelectedFreq(Number(e.target.value))}
            className="w-24 bg-gray-700 text-gray-200 border border-gray-600 rounded px-2 py-1 text-sm"
          />
          <span className="text-sm text-gray-400">Hz</span>
          {/* Quick presets */}
          <div className="flex gap-1">
            {[100, 500, 1000, 2000, 5000, 10000].map((f) => (
              <button
                key={f}
                onClick={() => setSelectedFreq(f)}
                className={`px-2 py-1 rounded text-xs ${
                  selectedFreq === f
                    ? 'bg-indigo-600 text-white'
                    : 'bg-gray-700 text-gray-400 hover:bg-gray-600'
                }`}
              >
                {f >= 1000 ? `${f / 1000}k` : f}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Tab content */}
      <div className="p-4 bg-gray-800 rounded-lg border border-gray-700">
        {activeTab === 'contour' && <ContourPlot spectra={spectra} />}
        {activeTab === 'frequency' && (
          <FrequencyResponsePlot spectra={spectra} showSoundPower />
        )}
        {activeTab === 'polar' && (
          <PolarAtFrequency spectra={spectra} frequencyHz={selectedFreq} />
        )}
        {activeTab === 'di' && <DirectivityIndexPlot spectra={spectra} />}
        {activeTab === 'balloon' && (
          <DirectivityBalloon spectra={spectra} frequencyHz={selectedFreq} />
        )}
        {activeTab === 'broadband' && <PolarPlot data={splData} size={500} />}
      </div>

      {/* CEA-2034 Metrics card */}
      {metrics && (
        <div className="p-4 bg-gray-800 rounded-lg border border-gray-700 space-y-3">
          <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wide">
            Approximate Directivity Metrics (CEA-2034)
          </h2>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 text-sm">
            <div className="p-3 bg-gray-900 rounded border border-gray-700">
              <div className="text-gray-500 text-xs">On-Axis</div>
              <div className="text-white font-mono">
                {isFinite(metrics.onAxisDb) ? `${metrics.onAxisDb.toFixed(1)} dB` : '--'}
              </div>
            </div>
            <div className="p-3 bg-gray-900 rounded border border-gray-700">
              <div className="text-gray-500 text-xs">Listening Window</div>
              <div className="text-white font-mono">
                {isFinite(metrics.listeningWindowDb)
                  ? `${metrics.listeningWindowDb.toFixed(1)} dB`
                  : '--'}
              </div>
            </div>
            <div className="p-3 bg-gray-900 rounded border border-gray-700">
              <div className="text-gray-500 text-xs">Early Reflections</div>
              <div className="text-white font-mono">
                {isFinite(metrics.earlyReflectionsDb)
                  ? `${metrics.earlyReflectionsDb.toFixed(1)} dB`
                  : '--'}
              </div>
            </div>
            <div className="p-3 bg-gray-900 rounded border border-gray-700">
              <div className="text-gray-500 text-xs">Sound Power</div>
              <div className="text-white font-mono">
                {isFinite(metrics.soundPowerDb)
                  ? `${metrics.soundPowerDb.toFixed(1)} dB`
                  : '--'}
              </div>
            </div>
            <div className="p-3 bg-gray-900 rounded border border-gray-700">
              <div className="text-gray-500 text-xs">Directivity Index</div>
              <div className="text-white font-mono">
                {isFinite(metrics.directivityIndexDb)
                  ? `${metrics.directivityIndexDb.toFixed(1)} dB`
                  : '--'}
              </div>
            </div>
            <div className="p-3 bg-gray-900 rounded border border-gray-700">
              <div className="text-gray-500 text-xs">Data Points</div>
              <div className="text-white font-mono">{metrics.measurementCount}</div>
            </div>
          </div>
          <p className="text-xs text-gray-600">
            Approximated from {measurements.length} azimuth positions x 5 elevations.
            Full CEA-2034 requires 70-point sphere with frequency-dependent data.
          </p>
        </div>
      )}

      <ExportPanel />
    </div>
  );
}
