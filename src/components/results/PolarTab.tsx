import { useEffect, useMemo, useState } from 'react';
import { api } from '../../api/client';
import type { AcousticInPoint, FFTResponse } from '../../api/types';
import { REPEATS_HELP } from '../../content/parameterHelp';
import { InfoToggle } from '../ui/InfoToggle';
import { type LevelSource, levelForSource } from './levelSource';
import { LevelSourceSelector } from './LevelSourceSelector';
import { type CompareSeries, type CompareSeriesApi, SeriesPicker } from './compareSeries';
import {
  DEFAULT_BAND,
  FrequencyBandSelector,
  type FreqBand,
} from './FrequencyBandSelector';
import { type PolarPoint, PolarPlotFrame, type PolarSeries } from './PolarPlot';

interface Props {
  compare: CompareSeriesApi;
}

const FFT_SETTINGS = { window: 'hann' as const, size: 4096, overlap: 0.5 };
const REPEAT_DASH = ['solid', 'dash', 'dashdot'] as const;

/** Mic list of each repeat in a series, one mic per elevation (first capture wins,
 *  as in the server's merged list). Old data without a repeat field is repeat 1. */
function micsByRepeat(s: CompareSeries): Map<number, AcousticInPoint[]> {
  const out = new Map<number, AcousticInPoint[]>();
  for (const u of s.underlying ?? []) {
    for (const a of u.acoustic) {
      const r = a.repeat ?? u.repeat ?? 1;
      const list = out.get(r) ?? [];
      if (!list.some((x) => x.elevation_deg === a.elevation_deg)) list.push(a);
      out.set(r, list);
    }
  }
  return new Map([...out.entries()].sort(([a], [b]) => a - b));
}

export function PolarTab({ compare }: Props) {
  const { series, keys, labelForKey, addSeries, removeSeries } = compare;
  const [ffts, setFfts] = useState<Record<string, FFTResponse>>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [band, setBand] = useState<FreqBand>(DEFAULT_BAND);
  const [source, setSource] = useState<LevelSource>({ kind: 'band' });
  const [rangeMode, setRangeMode] = useState<180 | 360>(180);
  const [showRepeats, setShowRepeats] = useState(false);

  const repeatsBySeries = useMemo(
    () => new Map(series.map((s) => [s.id, micsByRepeat(s)])),
    [series],
  );
  const anyRepeats = [...repeatsBySeries.values()].some((m) => m.size > 1);

  // Fetch FFTs for every mic of every repeat across every series (cache-keyed by measurement id).
  const allAcoustic = useMemo(() => {
    const seen = new Set<string>();
    const out: { keySlug: string; id: string }[] = [];
    for (const s of series) {
      const repeatMics = [...(repeatsBySeries.get(s.id)?.values() ?? [])].flat();
      for (const a of [...s.acoustic, ...repeatMics]) {
        if (seen.has(a.id)) continue;
        seen.add(a.id);
        out.push({ keySlug: s.keySlug, id: a.id });
      }
    }
    return out;
  }, [series, repeatsBySeries]);
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
    const level = (a: AcousticInPoint): number => {
      const fft = ffts[a.id];
      return fft ? levelForSource(fft, source, band) : Number.NaN;
    };
    const toPoints = (mics: AcousticInPoint[]): PolarPoint[] =>
      mics
        .map((a): PolarPoint => ({ elevation_deg: a.elevation_deg, spl_db: level(a), mic_serial: a.mic_serial }))
        .filter((p) => Number.isFinite(p.spl_db))
        .sort((a, b) => b.elevation_deg - a.elevation_deg);

    return series.flatMap((s: CompareSeries): PolarSeries[] => {
      const byRepeat = repeatsBySeries.get(s.id) ?? new Map<number, AcousticInPoint[]>();
      if (byRepeat.size <= 1) {
        return [{ label: s.label, color: s.color, points: toPoints(s.acoustic) }];
      }
      if (showRepeats) {
        return [...byRepeat.entries()].map(([r, mics]) => ({
          label: `${s.label} · repeat ${r}`,
          color: s.color,
          dash: REPEAT_DASH[(r - 1) % REPEAT_DASH.length],
          points: toPoints(mics),
        }));
      }
      // Off: per elevation, the mean dB level over the repeats that have that mic.
      const byElev = new Map<number, { serial: string; levels: number[] }>();
      for (const mics of byRepeat.values()) {
        for (const a of mics) {
          const l = level(a);
          if (!Number.isFinite(l)) continue;
          const e = byElev.get(a.elevation_deg) ?? { serial: a.mic_serial, levels: [] };
          e.levels.push(l);
          byElev.set(a.elevation_deg, e);
        }
      }
      const points = [...byElev.entries()]
        .map(([elev, e]): PolarPoint => ({
          elevation_deg: elev,
          spl_db: e.levels.reduce((x, y) => x + y, 0) / e.levels.length,
          mic_serial: e.serial,
        }))
        .sort((a, b) => b.elevation_deg - a.elevation_deg);
      return [{ label: `${s.label} · mean of ${byRepeat.size} repeats`, color: s.color, points }];
    });
  }, [series, repeatsBySeries, showRepeats, ffts, band, source]);

  const allAbsolute =
    allAcoustic.length > 0 && allAcoustic.every((a) => ffts[a.id]?.absolute_spl);
  const mixedAbsolute = allAcoustic.some((a) => ffts[a.id]?.absolute_spl) && !allAbsolute;
  // Response curve applied but no Sens Factor → still dBFS, must not be labelled SPL.
  const curveOnly = allAcoustic.some(
    (a) => ffts[a.id]?.calibrated && !ffts[a.id]?.absolute_spl,
  );
  const unit = allAbsolute ? 'dB SPL' : 'dBFS';
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
      <LevelSourceSelector source={source} onChange={setSource} ffts={Object.values(ffts)} />

      <div className="flex items-center justify-between gap-4 flex-wrap">
        <div className="text-xs text-gray-400">
          {source.kind === 'tone'
            ? <>Level: <span className="font-mono text-gray-200">BPF harmonic {source.harmonic}</span></>
            : <>Band: <span className="font-mono text-gray-200">{Math.round(band.low_hz)}–{Math.round(band.high_hz)} Hz</span>{source.kind === 'broadband' ? ', tones notched' : ''}</>}
          {' · '}
          {drawable.length} curve{drawable.length === 1 ? '' : 's'}
          {' · '}
          <span className={allAbsolute ? 'text-emerald-400' : 'text-gray-400'}>{unit}</span>
        </div>
        <div className="flex items-center gap-3">
          <label
            className={`inline-flex items-center gap-1.5 text-xs ${anyRepeats ? 'text-gray-300' : 'text-gray-500'}`}
            title={anyRepeats ? undefined : 'None of these captures has more than one repeat'}
          >
            <input
              type="checkbox"
              checked={showRepeats}
              disabled={!anyRepeats}
              onChange={(e) => setShowRepeats(e.target.checked)}
            />
            Show all repeats
            <InfoToggle label="repeats">{REPEATS_HELP}</InfoToggle>
          </label>
          <RangeModeToggle value={rangeMode} onChange={setRangeMode} />
        </div>
      </div>

      {mixedAbsolute && (
        <div className="text-xs text-amber-400 bg-amber-500/10 border border-amber-500/30 rounded-md p-2">
          ⚠ Mixing absolute (dB SPL) and relative (dBFS) series — absolute levels aren't comparable across these curves.
        </div>
      )}

      {curveOnly && (
        <div className="text-xs text-amber-400 bg-amber-500/10 border border-amber-500/30 rounded-md p-2">
          ⚠ Some calibration files carry no Sens Factor — only the frequency-response curve is
          applied to those, so their levels stay dBFS-relative, not dB SPL.
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
          <PolarPlotFrame series={drawable} rangeMode={rangeMode} unit={unit} />
        )}
      </div>
    </div>
  );
}

export function RangeModeToggle({
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
