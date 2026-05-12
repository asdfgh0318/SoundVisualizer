import { useEffect, useState } from 'react';
import { api } from '../../api/client';
import type { PerformanceSummary, PWMPoint } from '../../api/types';

interface Props {
  keySlug: string;
  point: PWMPoint;
}

export function PerformanceHeader({ keySlug, point }: Props) {
  const [summary, setSummary] = useState<PerformanceSummary | null>(null);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    setSummary(null);
    setError(null);
    if (!point.performance_id) return;
    let cancelled = false;
    api.getPerformanceSummary(keySlug, point.performance_id).then(
      (s) => !cancelled && setSummary(s),
      (e) => !cancelled && setError(e),
    );
    return () => { cancelled = true; };
  }, [keySlug, point.performance_id]);

  return (
    <div className="bg-gray-800 border border-gray-700 rounded-md p-4">
      <div className="flex items-baseline gap-3 mb-3">
        <span className="text-xs uppercase tracking-wide text-amber-400">PWM</span>
        <span className="text-2xl font-bold text-white font-mono">
          {point.pwm_us ?? '—'} <span className="text-gray-400 text-base">µs</span>
        </span>
        <span
          className={`text-[10px] uppercase tracking-wide px-2 py-0.5 rounded ${
            point.half === 'top'
              ? 'bg-sky-500/20 text-sky-300'
              : 'bg-rose-500/20 text-rose-300'
          }`}
        >
          {point.half ?? '—'} half
        </span>
      </div>

      {!point.performance_id && (
        <div className="text-sm text-gray-500 italic">No performance measurement at this point.</div>
      )}
      {error && <div className="text-sm text-red-400">Error: {error.message}</div>}
      {point.performance_id && !summary && !error && (
        <div className="text-sm text-gray-400 italic">Loading…</div>
      )}
      {summary && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <Stat label="Thrust (mean)" value={summary.thrust_n_mean.toFixed(2)} unit="N" />
          <Stat label="Torque (mean)" value={summary.torque_nm_mean.toFixed(3)} unit="N·m" />
          <Stat label="Current (mean)" value={summary.current_a_mean.toFixed(2)} unit="A" />
          <Stat label="Voltage (mean)" value={summary.voltage_v_mean.toFixed(2)} unit="V" />
          <Stat label="RPM (mean)" value={summary.rpm_mean.toFixed(0)} unit="" />
          <Stat label="Temp 0 (max)" value={summary.temp0_c_max.toFixed(1)} unit="°C" />
          <Stat label="Duration" value={summary.duration_s.toFixed(2)} unit="s" />
          <Stat label="Samples" value={summary.n_samples.toString()} unit="" />
        </div>
      )}
    </div>
  );
}

function Stat({ label, value, unit }: { label: string; value: string; unit: string }) {
  return (
    <div>
      <div className="text-[11px] uppercase tracking-wide text-gray-500">{label}</div>
      <div className="text-gray-100 text-base font-mono mt-0.5">
        {value}
        {unit && <span className="text-gray-500 text-xs ml-1">{unit}</span>}
      </div>
    </div>
  );
}
