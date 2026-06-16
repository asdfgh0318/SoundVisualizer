import type { MergedPWMPoint, PerformanceSummary } from '../../api/types';

interface Props {
  point: MergedPWMPoint;
  drilldownTStart: string | null;
}

export function PerformanceHeader({ point, drilldownTStart }: Props) {
  // If drilled into a specific underlying capture, use its perf summary;
  // otherwise use the group's averaged summary.
  let summary: PerformanceSummary | null = point.avg_performance;
  let label = 'Merged perf (mean across captures)';
  if (drilldownTStart) {
    const u = point.underlying.find((u) => u.t_start === drilldownTStart);
    if (u) {
      summary = u.performance_summary;
      label = `Drilled into ${u.half} capture · ${u.t_start.slice(11, 19)}`;
    }
  } else if (point.underlying.length === 1) {
    label = `${point.underlying[0].half} capture`;
  }

  return (
    <div className="bg-gray-800 border border-gray-700 rounded-md p-4">
      <div className="flex items-baseline gap-3 mb-3">
        <span className="text-xs uppercase tracking-wide text-amber-400">PWM</span>
        <span className="text-2xl font-bold text-white font-mono">
          {point.pwm_us} <span className="text-gray-400 text-base">µs</span>
        </span>
        <CompositionPill composition={point.composition} drilled={drilldownTStart !== null} />
      </div>

      <div className="text-xs text-gray-500 mb-2">{label}</div>

      {!summary && (
        <div className="text-sm text-gray-500 italic">No performance measurement at this point.</div>
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

function CompositionPill({
  composition, drilled,
}: {
  composition: Record<string, number>;
  drilled: boolean;
}) {
  if (drilled) {
    return (
      <span className="text-[10px] uppercase tracking-wide px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/40">
        drilled-in
      </span>
    );
  }
  const full = composition.full ?? 0;
  const top = composition.top ?? 0;
  const bot = composition.bottom ?? 0;
  const total = full + top + bot;

  // New single-pass captures (full > 0): show simple "Nx" count or "single capture".
  if (full > 0 && top === 0 && bot === 0) {
    return (
      <span className="text-[10px] uppercase tracking-wide px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300">
        {full === 1 ? 'single capture' : `${full}× captures`}
      </span>
    );
  }
  // Legacy two-pass merge: same labels as before, for backward compatibility.
  if (top > 0 && bot > 0) {
    if (top === 1 && bot === 1) {
      return (
        <span className="text-[10px] uppercase tracking-wide px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300">
          TOP + BOTTOM
        </span>
      );
    }
    return (
      <span className="text-[10px] uppercase tracking-wide px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300">
        {`${top} TOP + ${bot} BOTTOM`}
      </span>
    );
  }
  if (total === 1 && (top > 0 || bot > 0)) {
    return (
      <span className="text-[10px] uppercase tracking-wide px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/40">
        {top > 0 ? 'TOP only' : 'BOTTOM only'}
      </span>
    );
  }
  // Fallback: render whatever's there.
  const parts = Object.entries(composition).map(([k, v]) => `${v} ${k.toUpperCase()}`);
  return (
    <span className="text-[10px] uppercase tracking-wide px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300">
      {parts.join(' + ') || 'no data'}
    </span>
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
