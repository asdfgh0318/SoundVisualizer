import { useMemo } from 'react';

const ONE_THIRD = Math.pow(2, 1 / 6);
const SQRT_TWO = Math.SQRT2;

const THIRD_CENTERS = [
  20, 25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630,
  800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000,
  12500, 16000, 20000,
];
const OCTAVE_CENTERS = [31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000];

export const FREQ_MIN = 20;
export const FREQ_MAX = 24000;

export interface FreqBand {
  low_hz: number;
  high_hz: number;
}

export const DEFAULT_BAND: FreqBand = { low_hz: 100, high_hz: 10000 };

export function thirdOctaveBand(fc: number): FreqBand {
  return { low_hz: fc / ONE_THIRD, high_hz: fc * ONE_THIRD };
}

export function octaveBand(fc: number): FreqBand {
  return { low_hz: fc / SQRT_TWO, high_hz: fc * SQRT_TWO };
}

interface Props {
  band: FreqBand;
  onChange: (b: FreqBand) => void;
}

export function FrequencyBandSelector({ band, onChange }: Props) {
  const activeThird = useMemo(
    () =>
      THIRD_CENTERS.find((fc) => {
        const b = thirdOctaveBand(fc);
        return Math.abs(b.low_hz - band.low_hz) < 0.01 && Math.abs(b.high_hz - band.high_hz) < 0.01;
      }),
    [band],
  );
  const activeOctave = useMemo(
    () =>
      OCTAVE_CENTERS.find((fc) => {
        const b = octaveBand(fc);
        return Math.abs(b.low_hz - band.low_hz) < 0.01 && Math.abs(b.high_hz - band.high_hz) < 0.01;
      }),
    [band],
  );

  return (
    <div className="grid grid-cols-3 gap-3 bg-gray-800 border border-gray-700 rounded-md p-3">
      <ManualBand band={band} onChange={onChange} />
      <BandList
        title="1/3 octave"
        centers={THIRD_CENTERS}
        active={activeThird ?? null}
        onSelect={(fc) => onChange(thirdOctaveBand(fc))}
      />
      <BandList
        title="Octave"
        centers={OCTAVE_CENTERS}
        active={activeOctave ?? null}
        onSelect={(fc) => onChange(octaveBand(fc))}
      />
    </div>
  );
}

function ManualBand({ band, onChange }: Props) {
  const handle = (k: 'low_hz' | 'high_hz') => (e: React.ChangeEvent<HTMLInputElement>) => {
    const v = Number(e.target.value);
    if (!Number.isFinite(v)) return;
    const clamped = Math.max(FREQ_MIN, Math.min(FREQ_MAX, v));
    onChange({ ...band, [k]: clamped });
  };

  return (
    <div className="space-y-2">
      <div className="text-[11px] uppercase tracking-wide text-gray-500">Range</div>
      <label className="block">
        <span className="text-xs text-gray-400">High (Hz)</span>
        <input
          type="number"
          className="input w-full font-mono mt-0.5"
          min={FREQ_MIN}
          max={FREQ_MAX}
          step={1}
          value={Math.round(band.high_hz)}
          onChange={handle('high_hz')}
        />
      </label>
      <div className="h-24 relative bg-gray-900/60 rounded">
        {/* visual indicator: log-scale band on a vertical bar */}
        <div
          className="absolute inset-x-0 bg-indigo-500/40 border-y border-indigo-400"
          style={{
            top: `${pctFromTop(band.high_hz)}%`,
            bottom: `${100 - pctFromTop(band.low_hz)}%`,
          }}
        />
      </div>
      <label className="block">
        <span className="text-xs text-gray-400">Low (Hz)</span>
        <input
          type="number"
          className="input w-full font-mono mt-0.5"
          min={FREQ_MIN}
          max={FREQ_MAX}
          step={1}
          value={Math.round(band.low_hz)}
          onChange={handle('low_hz')}
        />
      </label>
    </div>
  );
}

function pctFromTop(hz: number): number {
  const lo = Math.log10(FREQ_MIN);
  const hi = Math.log10(FREQ_MAX);
  const v = Math.log10(Math.max(FREQ_MIN, Math.min(FREQ_MAX, hz)));
  // top of bar = high freq (FREQ_MAX), bottom = FREQ_MIN
  return ((hi - v) / (hi - lo)) * 100;
}

function BandList({
  title,
  centers,
  active,
  onSelect,
}: {
  title: string;
  centers: number[];
  active: number | null;
  onSelect: (fc: number) => void;
}) {
  return (
    <div className="flex flex-col min-h-0">
      <div className="text-[11px] uppercase tracking-wide text-gray-500 mb-1">{title}</div>
      <div className="overflow-y-auto max-h-[15rem] pr-1 space-y-0.5 scrollbar-thin">
        {centers.map((fc) => {
          const isActive = active === fc;
          return (
            <button
              key={fc}
              type="button"
              onClick={() => onSelect(fc)}
              className={`w-full text-left px-2 py-1 rounded text-xs font-mono transition-colors ${
                isActive
                  ? 'bg-indigo-600/40 border border-indigo-500/60 text-white'
                  : 'border border-transparent text-gray-300 hover:bg-gray-700/40 hover:text-white'
              }`}
            >
              {formatFreq(fc)} Hz
            </button>
          );
        })}
      </div>
    </div>
  );
}

function formatFreq(hz: number): string {
  if (hz >= 1000) return `${(hz / 1000).toLocaleString('en', { maximumFractionDigits: 2 })}k`;
  return hz.toString();
}
