import { WS_BASE } from '../../api/base';
import type { TelemetryFrame } from '../../api/types';
import { useWebSocketJson } from '../../hooks/useWebSocketJson';

interface Props {
  active: boolean;
}

export function LiveTelemetry({ active }: Props) {
  const url = active ? `${WS_BASE}/tyto/ws/telemetry` : null;
  const { message, state } = useWebSocketJson<TelemetryFrame>(url, active);

  return (
    <div className="bg-gray-900/60 border border-gray-700 rounded-md overflow-hidden">
      <div className="px-3 py-2 border-b border-gray-700 flex items-center justify-between text-xs">
        <span className="uppercase tracking-wide text-gray-400">Tyto telemetry</span>
        <span className="flex items-center gap-2">
          <span
            className={`inline-block w-2 h-2 rounded-full ${
              state === 'open'
                ? 'bg-green-500'
                : state === 'connecting'
                  ? 'bg-amber-500 animate-pulse'
                  : 'bg-gray-500'
            }`}
          />
          <span className="text-gray-400">{state}</span>
        </span>
      </div>
      <div className="p-3 grid grid-cols-2 sm:grid-cols-4 gap-3 text-sm">
        <Cell label="PWM" value={message ? `${message.pwm_us}` : '—'} unit="µs" />
        <Cell label="Thrust" value={message ? message.thrust_n.toFixed(2) : '—'} unit="N" />
        <Cell label="Torque" value={message ? message.torque_nm.toFixed(3) : '—'} unit="N·m" />
        <Cell label="RPM" value={message ? message.rpm.toFixed(0) : '—'} unit="" />
        <Cell label="Current" value={message ? message.current_a.toFixed(2) : '—'} unit="A" />
        <Cell label="Voltage" value={message ? message.voltage_v.toFixed(2) : '—'} unit="V" />
        <Cell label="Temp 0" value={message ? message.temp0_c.toFixed(1) : '—'} unit="°C" />
        <Cell label="Vibration" value={message ? `${message.vibration}` : '—'} unit="" />
      </div>
      {message?.tripped && (
        <div className="px-3 py-2 border-t border-red-700/60 bg-red-900/30 text-red-300 text-xs">
          Tripped on <strong>{message.tripped}</strong> — PWM forced to 1000 µs.
        </div>
      )}
    </div>
  );
}

function Cell({ label, value, unit }: { label: string; value: string; unit: string }) {
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
