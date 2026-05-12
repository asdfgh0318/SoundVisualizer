import { useEffect, useState } from 'react';
import { api, ApiError } from '../api/client';
import type { PWMPoint } from '../api/types';
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
  const [points, setPoints] = useState<PWMPoint[] | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [selectedT, setSelectedT] = useState<string | null>(null);
  const [reloadKey, setReloadKey] = useState(0);

  useEffect(() => {
    let cancelled = false;
    setPoints(null);
    setError(null);
    setSelectedT(null);
    api.listPWMPoints(keySlug).then(
      (p) => {
        if (cancelled) return;
        setPoints(p);
        if (p.length > 0) setSelectedT(p[0].t_start);
      },
      (e: Error | ApiError) => !cancelled && setError(e),
    );
    return () => { cancelled = true; };
  }, [keySlug, reloadKey]);

  if (error) return <div className="text-sm text-red-400">Error: {error.message}</div>;
  if (!points) return <div className="text-sm text-gray-400 italic">Loading PWM points…</div>;
  if (points.length === 0) {
    return (
      <div className="text-sm text-gray-400 italic">
        No measurements under this key yet.
      </div>
    );
  }

  const selected = points.find((p) => p.t_start === selectedT) ?? points[0];

  return (
    <div className="grid grid-cols-1 lg:grid-cols-[280px_1fr] gap-4">
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
          selectedT={selected.t_start}
          onSelect={setSelectedT}
        />
      </aside>

      <div className="space-y-4 min-w-0">
        <PerformanceHeader keySlug={keySlug} point={selected} />
        {tab === 'fft' && <FFTTab keySlug={keySlug} point={selected} />}
        {tab === 'polar' && (
          <PolarTab keySlug={keySlug} point={selected} allPoints={points} />
        )}
        {tab === 'custom' && (
          <CustomTab
            keySlug={keySlug}
            points={points}
            selectedT={selected.t_start}
            onSelectT={setSelectedT}
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
