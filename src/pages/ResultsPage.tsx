import { useEffect, useMemo, useState } from 'react';
import { api, ApiError } from '../api/client';
import type { MergedPWMPoint } from '../api/types';
import { CustomTab } from '../components/results/CustomTab';
import { FFTTab } from '../components/results/FFTTab';
import { KeyPicker } from '../components/results/KeyPicker';
import { PerformanceHeader } from '../components/results/PerformanceHeader';
import { PolarTab } from '../components/results/PolarTab';
import { PWMPointSidebar } from '../components/results/PWMPointSidebar';

type Tab = 'fft' | 'polar' | 'custom';

export function ResultsPage() {
  const [keySlug, setKeySlug] = useState<string | null>(null);
  const [tab, setTab] = useState<Tab>('fft');

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <header>
        <h1 className="text-2xl font-bold text-white">Results</h1>
        <p className="text-sm text-gray-400 mt-1">
          Group acoustic + performance measurements by PWM point and inspect spectra.
        </p>
      </header>

      <div className="flex items-center justify-between gap-4 flex-wrap">
        <KeyPicker value={keySlug} onChange={setKeySlug} />
        <Tabs value={tab} onChange={setTab} />
      </div>

      {keySlug ? (
        <ResultsBody keySlug={keySlug} tab={tab} />
      ) : (
        <div className="text-sm text-gray-400 italic">Pick a key to see results.</div>
      )}
    </div>
  );
}

function ResultsBody({ keySlug, tab }: { keySlug: string; tab: Tab }) {
  const [points, setPoints] = useState<MergedPWMPoint[] | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [drilldownTStart, setDrilldownTStart] = useState<string | null>(null);
  const [reloadKey, setReloadKey] = useState(0);

  useEffect(() => {
    let cancelled = false;
    setPoints(null);
    setError(null);
    setSelectedId(null);
    setDrilldownTStart(null);
    api.listPWMPoints(keySlug).then(
      (p) => {
        if (cancelled) return;
        setPoints(p);
        if (p.length > 0) setSelectedId(p[0].id);
      },
      (e: Error | ApiError) => !cancelled && setError(e),
    );
    return () => { cancelled = true; };
  }, [keySlug, reloadKey]);

  // Build the "effective" point passed to the tabs. If drilled into a specific
  // underlying capture, synthesize a single-capture point; else use the merged.
  const effectivePoint = useMemo<MergedPWMPoint | null>(() => {
    if (!points) return null;
    const selected = points.find((p) => p.id === selectedId) ?? points[0];
    if (!selected) return null;
    if (!drilldownTStart) return selected;
    const u = selected.underlying.find((u) => u.t_start === drilldownTStart);
    if (!u) return selected;
    return {
      id: selected.id,
      pwm_us: selected.pwm_us,
      composition: { [u.half]: 1 },
      underlying: [u],
      acoustic: u.acoustic,
      avg_performance: u.performance_summary,
    };
  }, [points, selectedId, drilldownTStart]);

  if (error) return <div className="text-sm text-red-400">Error: {error.message}</div>;
  if (!points) return <div className="text-sm text-gray-400 italic">Loading PWM points…</div>;
  if (points.length === 0) {
    return (
      <div className="text-sm text-gray-400 italic">
        No measurements under this key yet.
      </div>
    );
  }
  if (!effectivePoint) return null;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-[300px_1fr] gap-4">
      <aside>
        <div className="flex items-center justify-between mb-2 px-1">
          <div className="text-xs uppercase tracking-wide text-gray-500">
            PWM points ({points.length})
          </div>
          <button
            type="button"
            onClick={() => setReloadKey((k) => k + 1)}
            className="text-xs text-gray-400 hover:text-gray-200"
            title="Refetch measurements from server"
          >
            ↻ refresh
          </button>
        </div>
        <PWMPointSidebar
          points={points}
          selectedId={selectedId ?? points[0].id}
          drilldownTStart={drilldownTStart}
          onSelect={(id) => { setSelectedId(id); setDrilldownTStart(null); }}
          onDrilldown={(_mergedId, t) => setDrilldownTStart(t)}
        />
      </aside>

      <div className="space-y-4 min-w-0">
        <PerformanceHeader point={effectivePoint} drilldownTStart={drilldownTStart} />
        {tab === 'fft' && <FFTTab keySlug={keySlug} point={effectivePoint} />}
        {tab === 'polar' && <PolarTab keySlug={keySlug} point={effectivePoint} />}
        {tab === 'custom' && (
          <CustomTab
            keySlug={keySlug}
            points={points}
            selectedId={selectedId ?? points[0].id}
            onSelectId={(id) => { setSelectedId(id); setDrilldownTStart(null); }}
          />
        )}
      </div>
    </div>
  );
}

function Tabs({ value, onChange }: { value: Tab; onChange: (t: Tab) => void }) {
  const tabs: { key: Tab; label: string }[] = [
    { key: 'fft', label: 'FFT' },
    { key: 'polar', label: 'Polar' },
    { key: 'custom', label: 'Custom' },
  ];
  return (
    <div className="flex bg-gray-800 border border-gray-700 rounded-md overflow-hidden">
      {tabs.map((t) => (
        <button
          key={t.key}
          onClick={() => onChange(t.key)}
          className={`px-4 py-2 text-sm font-medium transition-colors ${
            value === t.key
              ? 'bg-indigo-600 text-white'
              : 'text-gray-300 hover:bg-gray-700 hover:text-white'
          }`}
        >
          {t.label}
        </button>
      ))}
    </div>
  );
}
