import type { Data, Layout, PlotMouseEvent } from 'plotly.js';
import { useEffect, useMemo, useState } from 'react';
import { api } from '../../api/client';
import type {
  FFTResponse,
  MergedPWMPoint,
  PerformanceSummary,
} from '../../api/types';
import { PlotlyChart } from '../ui/PlotlyChart';
import {
  DEFAULT_BAND,
  FrequencyBandSelector,
  type FreqBand,
} from './FrequencyBandSelector';

interface Props {
  keySlug: string;
  points: MergedPWMPoint[];
  selectedId: string | null;
  onSelectId: (id: string) => void;
}

const FFT_SETTINGS = { window: 'hann' as const, size: 4096, overlap: 0.5 };

type ColumnKey =
  | 'pwm_us'
  | 'thrust_n_mean'
  | 'thrust_n_max'
  | 'torque_nm_mean'
  | 'current_a_mean'
  | 'voltage_v_mean'
  | 'rpm_mean'
  | 'temp0_c_max'
  | 'spl_band';

const COLUMNS: { key: ColumnKey; label: string; unit: string }[] = [
  { key: 'pwm_us',         label: 'PWM',           unit: 'µs'  },
  { key: 'thrust_n_mean',  label: 'Thrust (mean)', unit: 'N'   },
  { key: 'thrust_n_max',   label: 'Thrust (max)',  unit: 'N'   },
  { key: 'torque_nm_mean', label: 'Torque (mean)', unit: 'N·m' },
  { key: 'current_a_mean', label: 'Current (mean)', unit: 'A'  },
  { key: 'voltage_v_mean', label: 'Voltage (mean)', unit: 'V'  },
  { key: 'rpm_mean',       label: 'RPM (mean)',    unit: ''    },
  { key: 'temp0_c_max',    label: 'Temp 0 (max)',  unit: '°C'  },
  { key: 'spl_band',       label: 'SPL (band)',    unit: 'dB'  },
];

interface Row {
  id: string;
  pwm_us: number;
  composition: Record<string, number>;
  perf: PerformanceSummary | null;
  spl_band: number | null;
}

const COL_MERGED = '#818cf8';  // indigo-400 — full T+B point
const COL_SINGLE = '#fda4af';  // rose-300 — only-one-half point
const COL_SELECTED = '#fbbf24'; // amber-400

export function CustomTab({ keySlug, points, selectedId, onSelectId }: Props) {
  const [ffts, setFfts] = useState<Record<string, FFTResponse>>({});
  const [fftError, setFftError] = useState<Error | null>(null);

  const [xCol, setXCol] = useState<ColumnKey>('thrust_n_mean');
  const [yCol, setYCol] = useState<ColumnKey>('spl_band');
  const [band, setBand] = useState<FreqBand>(DEFAULT_BAND);

  // Fetch FFTs for every acoustic measurement (lazy: only if SPL column needed).
  const splNeeded = xCol === 'spl_band' || yCol === 'spl_band' || selectedId !== null;
  useEffect(() => {
    if (!splNeeded) return;
    let cancelled = false;
    setFftError(null);
    const ids = points.flatMap((p) => p.acoustic.map((a) => a.id));
    Promise.all(
      ids.map((id) =>
        api.getFFT(keySlug, id, FFT_SETTINGS).then((r): [string, FFTResponse] => [id, r]),
      ),
    )
      .then((entries) => !cancelled && setFfts(Object.fromEntries(entries)))
      .catch((e: Error) => !cancelled && setFftError(e));
    return () => { cancelled = true; };
  }, [keySlug, points, splNeeded]);

  const rows = useMemo<Row[]>(
    () =>
      points.map((p) => {
        const splByMic = p.acoustic
          .map((a) => {
            const fft = ffts[a.id];
            if (!fft) return null;
            return bandPowerDb(fft.frequencies, fft.magnitudes_db, band.low_hz, band.high_hz);
          })
          .filter((v): v is number => v !== null);
        const spl = splByMic.length > 0 ? logMean(splByMic) : null;
        return {
          id: p.id,
          pwm_us: p.pwm_us,
          composition: p.composition,
          perf: p.avg_performance,
          spl_band: spl,
        };
      }),
    [points, ffts, band],
  );

  const selectedRow = rows.find((r) => r.id === selectedId) ?? null;
  const selectedPoint = points.find((p) => p.id === selectedId) ?? null;

  const onScatterClick = (e: PlotMouseEvent) => {
    const pt = e.points[0];
    if (!pt) return;
    const id = pt.customdata as string;
    if (typeof id === 'string') onSelectId(id);
  };

  return (
    <div className="space-y-4">
      <div className="bg-gray-800 border border-gray-700 rounded-md p-3 grid grid-cols-1 sm:grid-cols-3 gap-3">
        <AxisPicker label="X axis" value={xCol} onChange={setXCol} />
        <AxisPicker label="Y axis" value={yCol} onChange={setYCol} />
        <div className="text-xs text-gray-500 self-end">
          {(xCol === 'spl_band' || yCol === 'spl_band') ? (
            <>SPL band: <span className="font-mono text-gray-200">{Math.round(band.low_hz)}–{Math.round(band.high_hz)} Hz</span></>
          ) : (
            <>Pick "SPL (band)" on either axis to enable the band selector below.</>
          )}
        </div>
      </div>

      {(xCol === 'spl_band' || yCol === 'spl_band') && (
        <FrequencyBandSelector band={band} onChange={setBand} />
      )}

      {fftError && (
        <div className="text-sm text-red-400">FFT error: {fftError.message}</div>
      )}

      <div className="bg-gray-800 border border-gray-700 rounded-md p-3 space-y-2">
        <div className="flex items-center justify-end gap-4 text-xs px-1">
          <LegendSwatch color={COL_MERGED} label="full / merged" />
          <LegendSwatch color={COL_SINGLE} label="single-half only (legacy)" />
          <LegendSwatch color={COL_SELECTED} label="selected — click to change" big />
        </div>
        <ScatterPlot
          rows={rows}
          xCol={xCol}
          yCol={yCol}
          selectedId={selectedId}
          onClick={onScatterClick}
        />
      </div>

      {selectedRow && selectedPoint && (
        <SelectedPointFFTPanel
          row={selectedRow}
          point={selectedPoint}
          ffts={ffts}
        />
      )}
    </div>
  );
}

function LegendSwatch({
  color,
  label,
  big = false,
}: {
  color: string;
  label: string;
  big?: boolean;
}) {
  return (
    <span className="inline-flex items-center gap-1.5 text-gray-300">
      <span
        className="inline-block rounded-full border border-gray-900"
        style={{ background: color, width: big ? 12 : 8, height: big ? 12 : 8 }}
      />
      {label}
    </span>
  );
}

function AxisPicker({
  label,
  value,
  onChange,
}: {
  label: string;
  value: ColumnKey;
  onChange: (v: ColumnKey) => void;
}) {
  return (
    <label className="block">
      <span className="text-xs uppercase tracking-wide text-gray-400">{label}</span>
      <select
        className="input w-full mt-1"
        value={value}
        onChange={(e) => onChange(e.target.value as ColumnKey)}
      >
        {COLUMNS.map((c) => (
          <option key={c.key} value={c.key}>
            {c.label}
            {c.unit && ` (${c.unit})`}
          </option>
        ))}
      </select>
    </label>
  );
}

function ScatterPlot({
  rows, xCol, yCol, selectedId, onClick,
}: {
  rows: Row[];
  xCol: ColumnKey;
  yCol: ColumnKey;
  selectedId: string | null;
  onClick: (e: PlotMouseEvent) => void;
}) {
  const xLabel = COLUMNS.find((c) => c.key === xCol)!.label;
  const yLabel = COLUMNS.find((c) => c.key === yCol)!.label;

  const traces = useMemo<Data[]>(() => {
    const value = (r: Row, c: ColumnKey): number | null => {
      if (c === 'pwm_us') return r.pwm_us;
      if (c === 'spl_band') return r.spl_band;
      return r.perf ? (r.perf[c] as number) : null;
    };

    const compositionLabel = (comp: Record<string, number>): string => {
      const t = comp.top ?? 0;
      const b = comp.bottom ?? 0;
      const f = comp.full ?? 0;
      if (f > 0 && t === 0 && b === 0) return f === 1 ? 'full' : `${f}× full`;
      if (t === 1 && b === 1) return 'T+B';
      if (t === 0 && b > 0) return `${b}B`;
      if (b === 0 && t > 0) return `${t}T`;
      const parts: string[] = [];
      if (t > 0) parts.push(`${t}T`);
      if (b > 0) parts.push(`${b}B`);
      if (f > 0) parts.push(`${f}×`);
      return parts.join(' + ');
    };

    type Point = { x: number; y: number; text: string; customdata: string };
    const merged: Point[] = [];
    const single: Point[] = [];
    const selected: Point[] = [];

    for (const r of rows) {
      const xv = value(r, xCol);
      const yv = value(r, yCol);
      if (xv === null || yv === null) continue;
      const t = r.composition.top ?? 0;
      const b = r.composition.bottom ?? 0;
      const f = r.composition.full ?? 0;
      // "single-half" badge only meaningful for legacy two-pass data.
      const isSingleHalf = f === 0 && t + b === 1;
      const point: Point = {
        x: xv,
        y: yv,
        text: `PWM ${r.pwm_us} µs · ${compositionLabel(r.composition)}`,
        customdata: r.id,
      };
      if (r.id === selectedId) selected.push(point);
      else if (isSingleHalf) single.push(point);
      else merged.push(point);
    }

    const mk = (name: string, color: string, size: number, pts: Point[]): Data => ({
      type: 'scatter',
      mode: 'markers',
      name,
      x: pts.map((p) => p.x),
      y: pts.map((p) => p.y),
      text: pts.map((p) => p.text),
      customdata: pts.map((p) => p.customdata),
      marker: { color, size, line: { color: '#0f172a', width: 1 } },
      hovertemplate:
        '%{text}<br>%{xaxis.title.text}: %{x}<br>%{yaxis.title.text}: %{y:.3f}<extra></extra>',
    });

    return [
      mk('merged', COL_MERGED, 9, merged),
      mk('single-half', COL_SINGLE, 9, single),
      mk('selected', COL_SELECTED, 14, selected),
    ];
  }, [rows, xCol, yCol, selectedId]);

  const layout = useMemo<Partial<Layout>>(
    () => ({
      autosize: true,
      height: 400,
      paper_bgcolor: 'rgba(0,0,0,0)',
      plot_bgcolor: 'rgba(0,0,0,0)',
      margin: { l: 60, r: 20, t: 10, b: 50 },
      xaxis: {
        title: { text: xLabel, font: { color: '#9ca3af' } },
        gridcolor: '#374151',
        zerolinecolor: '#374151',
        tickfont: { color: '#9ca3af' },
      },
      yaxis: {
        title: { text: yLabel, font: { color: '#9ca3af' } },
        gridcolor: '#374151',
        zerolinecolor: '#374151',
        tickfont: { color: '#9ca3af' },
      },
      legend: {
        orientation: 'h',
        x: 0,
        y: 1.1,
        font: { color: '#d1d5db', size: 11 },
        bgcolor: 'rgba(0,0,0,0)',
      },
    }),
    [xLabel, yLabel],
  );

  return <PlotlyChart data={traces} layout={layout} className="w-full" onClick={onClick} />;
}

function SelectedPointFFTPanel({
  row,
  point,
  ffts,
}: {
  row: Row;
  point: MergedPWMPoint;
  ffts: Record<string, FFTResponse>;
}) {
  const traces = useMemo<Data[]>(() => {
    const palette = ['#818cf8', '#a78bfa', '#f472b6', '#fb923c', '#34d399', '#22d3ee'];
    return point.acoustic.map((a: typeof point.acoustic[number], i: number) => {
      const fft = ffts[a.id];
      const color = palette[i % palette.length];
      return {
        type: 'scatter',
        mode: 'lines',
        name: `${a.elevation_deg > 0 ? '+' : ''}${a.elevation_deg}°`,
        x: fft ? fft.frequencies.slice(1) : [],
        y: fft ? fft.magnitudes_db.slice(1) : [],
        line: { color, width: 1 },
        hovertemplate: `${a.elevation_deg}°<br>%{x:.0f} Hz<br>%{y:.1f} dB<extra></extra>`,
      } as Data;
    });
  }, [point.acoustic, ffts]);

  const layout = useMemo<Partial<Layout>>(
    () => ({
      autosize: true,
      height: 320,
      paper_bgcolor: 'rgba(0,0,0,0)',
      plot_bgcolor: 'rgba(0,0,0,0)',
      margin: { l: 50, r: 20, t: 10, b: 40 },
      xaxis: {
        type: 'log',
        range: [Math.log10(20), Math.log10(24000)],
        gridcolor: '#374151',
        tickfont: { color: '#9ca3af' },
        title: { text: 'Hz', font: { color: '#9ca3af' } },
      },
      yaxis: {
        gridcolor: '#374151',
        tickfont: { color: '#9ca3af' },
        title: { text: 'dB', font: { color: '#9ca3af' } },
      },
      legend: { orientation: 'h', font: { color: '#d1d5db', size: 11 } },
    }),
    [],
  );

  return (
    <div className="bg-gray-800 border border-gray-700 rounded-md p-3">
      <div className="flex items-baseline gap-3 mb-2 px-1">
        <span className="text-xs uppercase tracking-wide text-gray-500">Selected</span>
        <span className="text-sm font-mono text-gray-200">PWM {row.pwm_us} µs</span>
        {row.spl_band !== null && (
          <span className="text-xs text-gray-400">
            band SPL: <span className="font-mono text-gray-200">{row.spl_band.toFixed(1)} dB</span>
          </span>
        )}
      </div>
      {traces.length === 0 ? (
        <div className="text-sm text-gray-500 italic p-3">Loading FFTs…</div>
      ) : (
        <PlotlyChart data={traces} layout={layout} className="w-full" />
      )}
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

function logMean(dbValues: number[]): number {
  if (dbValues.length === 0) return -200;
  const meanPower = dbValues.reduce((s, db) => s + Math.pow(10, db / 10), 0) / dbValues.length;
  return 10 * Math.log10(meanPower);
}
