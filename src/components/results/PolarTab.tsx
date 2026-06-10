import { useEffect, useMemo, useState } from 'react';
import { api } from '../../api/client';
import type { FFTResponse } from '../../api/types';
import { type CompareSeries, type CompareSeriesApi, SeriesPicker } from './compareSeries';
import {
  DEFAULT_BAND,
  FrequencyBandSelector,
  type FreqBand,
} from './FrequencyBandSelector';
import { type PolarPoint, PolarPolarPlot, type PolarSeries } from './PolarPlot';

interface Props {
  compare: CompareSeriesApi;
}

const FFT_SETTINGS = { window: 'hann' as const, size: 4096, overlap: 0.5 };

export function PolarTab({ compare }: Props) {
  const { series, keys, labelForKey, addSeries, removeSeries } = compare;
  const [ffts, setFfts] = useState<Record<string, FFTResponse>>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [band, setBand] = useState<FreqBand>(DEFAULT_BAND);
  const [rangeMode, setRangeMode] = useState<180 | 360>(180);

  // Fetch FFTs for every mic across every series (cache-keyed by measurement id).
  const allAcoustic = useMemo(
    () => series.flatMap((s) => s.acoustic.map((a) => ({ keySlug: s.keySlug, id: a.id }))),
    [series],
  );
  const allIdsKey = allAcoustic.map((a) => a.id).join(',');

  useEffect(() => {
    let cancelled = false;
    setError(null);
    setLoading(true);
    Promise.all(
      allAcoustic.map((a) =>
        api.getFFT(a.keySlug, a.id, FFT_SETTINGS).then((r): [string, FFTResponse] => [a.id, r]),
      ),
    )
      .then((entries) => {
        if (cancelled) return;
        setFfts((prev) => ({ ...prev, ...Object.fromEntries(entries) }));
        setLoading(false);
      })
      .catch((e: Error) => {
        if (cancelled) return;
        setError(e);
        setLoading(false);
      });
    return () => { cancelled = true; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [allIdsKey]);

  const polarSeries = useMemo<PolarSeries[]>(() => {
    return series.map((s: CompareSeries): PolarSeries => ({
      label: s.label,
      color: s.color,
      points: s.acoustic
        .map((a): PolarPoint => {
          const fft = ffts[a.id];
          const spl = fft
            ? bandPowerDb(fft.frequencies, fft.magnitudes_db, band.low_hz, band.high_hz)
            : Number.NaN;
          return { elevation_deg: a.elevation_deg, spl_db: spl, mic_serial: a.mic_serial };
        })
        .filter((p) => Number.isFinite(p.spl_db))
        .sort((a, b) => b.elevation_deg - a.elevation_deg),
    }));
  }, [series, ffts, band]);

  const allCalibrated =
    allAcoustic.length > 0 && allAcoustic.every((a) => ffts[a.id]?.calibrated);
  const anyCalibrated = allAcoustic.some((a) => ffts[a.id]?.calibrated);
  const mixedCalibration = anyCalibrated && !allCalibrated;
  const drawable = polarSeries.filter((s) => s.points.length >= 2);

  return (
    <div className="space-y-4">
      <SeriesPicker
        keys={keys}
        series={series}
        baseId={series[0]?.id}
        labelForKey={labelForKey}
        onAdd={addSeries}
        onRemove={removeSeries}
      />

      <FrequencyBandSelector band={band} onChange={setBand} />

      <div className="flex items-center justify-between gap-4 flex-wrap">
        <div className="text-xs text-gray-400">
          Band: <span className="font-mono text-gray-200">{Math.round(band.low_hz)}–{Math.round(band.high_hz)} Hz</span>
          {' · '}
          {drawable.length} curve{drawable.length === 1 ? '' : 's'}
          {allCalibrated && (
            <span className="ml-2 text-emerald-400 uppercase tracking-wide text-[10px]">calibrated</span>
          )}
        </div>
        <RangeModeToggle value={rangeMode} onChange={setRangeMode} />
      </div>

      {mixedCalibration && (
        <div className="text-xs text-amber-400 bg-amber-500/10 border border-amber-500/30 rounded-md p-2">
          ⚠ Mixing calibrated (dB SPL) and uncalibrated (dBFS) series — absolute levels aren't comparable across these curves.
        </div>
      )}

      <div className="bg-gray-800 border border-gray-700 rounded-md p-3">
        {error && <div className="text-sm text-red-400 p-3">FFT error: {error.message}</div>}
        {loading && !error && (
          <div className="text-sm text-gray-400 italic p-3">Computing FFTs…</div>
        )}
        {!loading && !error && drawable.length === 0 && (
          <div className="text-sm text-gray-400 italic p-3">
            Not enough mics to draw a polar plot.
          </div>
        )}
        {!loading && !error && drawable.length > 0 && (
          <PolarPolarPlot series={drawable} rangeMode={rangeMode} />
        )}
      </div>
    </div>
  );
}

function RangeModeToggle({
  value, onChange,
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
