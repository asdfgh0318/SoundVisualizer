import { useEffect, useMemo, useState } from 'react';
import { api } from '../../api/client';
import type { AcousticInPoint, FFTResponse, PWMPoint } from '../../api/types';
import {
  DEFAULT_BAND,
  FrequencyBandSelector,
  type FreqBand,
} from './FrequencyBandSelector';
import { type PolarPoint, PolarPolarPlot } from './PolarPlot';

interface Props {
  keySlug: string;
  point: PWMPoint;
  allPoints: PWMPoint[];
}

const FFT_SETTINGS = { window: 'hann' as const, size: 4096, overlap: 0.5 };

function findSibling(point: PWMPoint, allPoints: PWMPoint[]): PWMPoint | null {
  if (point.pwm_us === null || point.half === null) return null;
  const otherHalf = point.half === 'top' ? 'bottom' : 'top';
  const t = Date.parse(point.t_start);
  const candidates = allPoints.filter(
    (p) => p.pwm_us === point.pwm_us && p.half === otherHalf,
  );
  if (candidates.length === 0) return null;
  candidates.sort(
    (a, b) =>
      Math.abs(Date.parse(a.t_start) - t) - Math.abs(Date.parse(b.t_start) - t),
  );
  return candidates[0];
}

export function PolarTab({ keySlug, point, allPoints }: Props) {
  const [ffts, setFfts] = useState<Record<string, FFTResponse>>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [band, setBand] = useState<FreqBand>(DEFAULT_BAND);
  const [rangeMode, setRangeMode] = useState<180 | 360>(180);
  const [mergeSibling, setMergeSibling] = useState(true);

  const sibling = useMemo(() => findSibling(point, allPoints), [point, allPoints]);
  const merging = mergeSibling && sibling !== null;

  const allAcoustic: AcousticInPoint[] = useMemo(
    () => (merging && sibling ? [...point.acoustic, ...sibling.acoustic] : point.acoustic),
    [point.acoustic, merging, sibling],
  );

  // Fetch FFT for every acoustic measurement in the combined set.
  useEffect(() => {
    let cancelled = false;
    setFfts({});
    setError(null);
    setLoading(true);
    Promise.all(
      allAcoustic.map((a) =>
        api.getFFT(keySlug, a.id, FFT_SETTINGS).then(
          (r): [string, FFTResponse] => [a.id, r],
        ),
      ),
    )
      .then((entries) => {
        if (cancelled) return;
        setFfts(Object.fromEntries(entries));
        setLoading(false);
      })
      .catch((e: Error) => {
        if (cancelled) return;
        setError(e);
        setLoading(false);
      });
    return () => { cancelled = true; };
  }, [keySlug, allAcoustic]);

  const polarPoints = useMemo<PolarPoint[]>(() => {
    return allAcoustic
      .map((a) => {
        const fft = ffts[a.id];
        const spl = fft
          ? bandPowerDb(fft.frequencies, fft.magnitudes_db, band.low_hz, band.high_hz)
          : Number.NaN;
        return {
          elevation_deg: a.elevation_deg,
          spl_db: spl,
          mic_serial: a.mic_serial,
        };
      })
      .filter((p) => Number.isFinite(p.spl_db))
      // Sort by elevation descending — required by PolarPlot.
      .sort((a, b) => b.elevation_deg - a.elevation_deg);
  }, [allAcoustic, ffts, band]);

  const allCalibrated =
    allAcoustic.length > 0 && allAcoustic.every((a) => ffts[a.id]?.calibrated);

  return (
    <div className="space-y-4">
      <FrequencyBandSelector band={band} onChange={setBand} />

      <div className="flex items-center justify-between gap-4 flex-wrap">
        <div className="text-xs text-gray-400">
          Band: <span className="font-mono text-gray-200">{Math.round(band.low_hz)}–{Math.round(band.high_hz)} Hz</span>
          {' · '}
          {polarPoints.length} mics
          {merging && (
            <span className="ml-2 px-1.5 py-0.5 rounded text-[10px] uppercase tracking-wide bg-indigo-500/20 text-indigo-300">
              top + bottom merged
            </span>
          )}
          {allCalibrated && (
            <span className="ml-2 text-emerald-400 uppercase tracking-wide text-[10px]">
              calibrated
            </span>
          )}
        </div>
        <div className="flex items-center gap-3">
          <SiblingToggle
            disabled={sibling === null}
            value={mergeSibling}
            onChange={setMergeSibling}
            sibling={sibling}
          />
          <RangeModeToggle value={rangeMode} onChange={setRangeMode} />
        </div>
      </div>

      <div className="bg-gray-800 border border-gray-700 rounded-md p-3">
        {error && <div className="text-sm text-red-400 p-3">FFT error: {error.message}</div>}
        {loading && !error && (
          <div className="text-sm text-gray-400 italic p-3">
            Computing FFTs for {allAcoustic.length} mics…
          </div>
        )}
        {!loading && !error && polarPoints.length < 2 && (
          <div className="text-sm text-gray-400 italic p-3">
            Not enough mics to draw a polar plot at this PWM point.
          </div>
        )}
        {!loading && !error && polarPoints.length >= 2 && (
          <PolarPolarPlot points={polarPoints} rangeMode={rangeMode} />
        )}
      </div>
    </div>
  );
}

function SiblingToggle({
  disabled,
  value,
  onChange,
  sibling,
}: {
  disabled: boolean;
  value: boolean;
  onChange: (v: boolean) => void;
  sibling: PWMPoint | null;
}) {
  const tooltip = disabled
    ? `No matching ${'top/bottom'} capture at this PWM µs`
    : sibling
      ? `Merge with ${sibling.half} capture at ${sibling.t_start.slice(11, 19)}`
      : '';
  return (
    <label
      className={`inline-flex items-center gap-2 text-xs ${
        disabled ? 'text-gray-600 cursor-not-allowed' : 'text-gray-300 cursor-pointer'
      }`}
      title={tooltip}
    >
      <input
        type="checkbox"
        disabled={disabled}
        checked={value && !disabled}
        onChange={(e) => onChange(e.target.checked)}
        className="accent-indigo-500 w-4 h-4 disabled:opacity-40"
      />
      Merge top + bottom
    </label>
  );
}

function RangeModeToggle({
  value,
  onChange,
}: {
  value: 180 | 360;
  onChange: (v: 180 | 360) => void;
}) {
  return (
    <div className="flex bg-gray-800 border border-gray-700 rounded-md overflow-hidden text-xs">
      {[180, 360].map((m) => (
        <button
          key={m}
          type="button"
          onClick={() => onChange(m as 180 | 360)}
          className={`px-3 py-1.5 font-medium transition-colors ${
            value === m ? 'bg-indigo-600 text-white' : 'text-gray-300 hover:bg-gray-700'
          }`}
        >
          {m}°
        </button>
      ))}
    </div>
  );
}

/** Integrate PSD over [low, high] Hz. mag_db is 10*log10(PSD). Returns total band power in dB. */
function bandPowerDb(freqs: number[], magsDb: number[], low: number, high: number): number {
  let totalPower = 0;
  for (let i = 0; i < freqs.length; i++) {
    const f = freqs[i];
    if (f < low || f > high) continue;
    const power = Math.pow(10, magsDb[i] / 10);
    const df =
      i + 1 < freqs.length
        ? freqs[i + 1] - freqs[i]
        : i > 0
          ? freqs[i] - freqs[i - 1]
          : 1;
    totalPower += power * df;
  }
  if (totalPower <= 0) return -200;
  return 10 * Math.log10(totalPower);
}
