import type { Data, Layout } from 'plotly.js';
import { useMemo, useState } from 'react';
import { PlotlyChart } from '../ui/PlotlyChart';
import { MicArcSchematic } from './MicArcSchematic';

export interface PolarPoint {
  elevation_deg: number;
  spl_db: number;
  mic_serial: string;
}

/** One directivity curve to draw = a labelled, colored set of polar points. */
export interface PolarSeries {
  label: string;
  color: string;
  points: PolarPoint[]; // sorted by elevation descending (+90 → -90)
}

interface Props {
  series: PolarSeries[];
  rangeMode: 180 | 360;
  /** "dB SPL" once a Sens Factor is applied, otherwise "dBFS". */
  unit: string;
  /** Bump to redraw the plot at its default range (a "reset view"). */
  resetKey?: number;
}

const POLAR_CONFIG = { scrollZoom: true, doubleClick: 'reset' as const };

const GRID = '#374151';
const TEXT = '#9ca3af';

const hoverTemplate = (unit: string) =>
  `%{fullData.name}<br>elev %{customdata[0]}° (%{customdata[1]})<br>%{r:.1f} ${unit}<extra></extra>`;

// Plotly default polar convention: theta=0 is at 3 o'clock (right), increases
// counter-clockwise. We want elevation = +90° at 12 o'clock, 0° at 3 o'clock,
// -90° at 6 o'clock. Negative elevations wrap below: -45 → 315, -90 → 270.
const elevToTheta = (e: number): number => (e >= 0 ? e : 360 + e);
// Mirror across the vertical axis (the 12-6 line): θ_mirror = 180 - θ_right.
const elevToMirrorTheta = (e: number): number => 180 - e;

export function PolarPolarPlot({ series, rangeMode, unit, resetKey = 0 }: Props) {
  const showLegend = series.length > 1;

  const data = useMemo<Data[]>(() => {
    const traces: Data[] = [];
    for (const s of series) {
      const pts = s.points;
      if (pts.length < 2) continue;
      const elevs = pts.map((p) => p.elevation_deg);
      const spls = pts.map((p) => p.spl_db);
      const serials = pts.map((p) => p.mic_serial);
      const cd = elevs.map((e, i): [number, string] => [e, serials[i]]);

      const base = {
        type: 'scatterpolar' as const,
        mode: 'lines+markers' as const,
        line: { color: s.color, width: 2 },
        marker: { color: s.color, size: 7 },
        hovertemplate: hoverTemplate(unit),
        name: s.label,
      };

      traces.push({ ...base, theta: elevs.map(elevToTheta), r: spls, customdata: cd, showlegend: showLegend });

      if (rangeMode === 360) {
        // Mirror trace shares the legend entry → don't double-list it.
        traces.push({ ...base, theta: elevs.map(elevToMirrorTheta), r: spls, customdata: cd, showlegend: false });
      }
    }
    return traces;
  }, [series, rangeMode, showLegend, unit]);

  // Anchor the centre of the plot at 0 so the radius reads as an absolute level
  // and every tick is positive. Only valid for real dB SPL — uncalibrated dBFS is
  // negative and would fall entirely outside a [0, max] range, so that stays
  // auto-scaled rather than silently rendering an empty chart.
  const radialRange = useMemo(() => {
    const vals = series.flatMap((s) => s.points.map((p) => p.spl_db)).filter(Number.isFinite);
    if (vals.length === 0 || Math.min(...vals) < 0) return {};
    const max = Math.max(...vals);
    const step = max <= 20 ? 5 : max <= 60 ? 10 : 20;
    return { range: [0, Math.ceil(max / step) * step], tick0: 0, dtick: step };
  }, [series]);

  const layout = useMemo<Partial<Layout>>(() => {
    // 180° mode: right half visible, ticks at 90/45/0/315/270 (+90 / +45 / 0 / -45 / -90).
    // 360° mode: full circle, also ticks for the mirror at 135/180/225 (+45 / 0 / -45).
    const ticks180 = [90, 45, 0, 315, 270];
    const labels180 = ['+90°', '+45°', '0°', '−45°', '−90°'];
    const ticks360 = [90, 45, 0, 315, 270, 225, 180, 135];
    const labels360 = ['+90°', '+45°', '0°', '−45°', '−90°', '−45°', '0°', '+45°'];

    return {
      autosize: true,
      height: 520,
      paper_bgcolor: 'rgba(0,0,0,0)',
      polar: {
        bgcolor: 'rgba(0,0,0,0)',
        radialaxis: {
          gridcolor: GRID,
          linecolor: GRID,
          tickfont: { color: TEXT, size: 10 },
          ticksuffix: ` ${unit}`,
          angle: 0,
          showline: true,
          ...radialRange,
        },
        angularaxis: {
          tickmode: 'array',
          tickvals: rangeMode === 360 ? ticks360 : ticks180,
          ticktext: rangeMode === 360 ? labels360 : labels180,
          gridcolor: GRID,
          linecolor: GRID,
          tickfont: { color: TEXT, size: 11 },
        },
        sector: rangeMode === 180 ? [270, 450] : [0, 360],
      },
      margin: { l: 40, r: 40, t: 30, b: 30 },
      showlegend: showLegend,
      legend: { orientation: 'h', x: 0, y: 1.08, font: { color: '#d1d5db', size: 11 }, bgcolor: 'rgba(0,0,0,0)' },
    };
    // resetKey is a dependency on purpose: a new layout object makes PlotlyChart
    // call newPlot again, which drops any zoom or pan the user applied.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [rangeMode, showLegend, unit, radialRange, resetKey]);

  return <PlotlyChart data={data} layout={layout} config={POLAR_CONFIG} className="w-full" />;
}

/** The polar plot with the mic-arc schematic beside it, a zoom hint and a
 *  reset button underneath. Both Results tabs that draw a polar use this. */
export function PolarPlotFrame({ series, rangeMode, unit }: Omit<Props, 'resetKey'>) {
  const [resetKey, setResetKey] = useState(0);
  const activeSerials = useMemo(
    () => Array.from(new Set(series.flatMap((s) => s.points.map((p) => p.mic_serial)))),
    [series],
  );
  return (
    <div className="space-y-2">
      <div className="flex gap-3">
        <div className="flex-1 min-w-0">
          <PolarPolarPlot series={series} rangeMode={rangeMode} unit={unit} resetKey={resetKey} />
        </div>
        <aside className="hidden md:block w-44 shrink-0 pt-2">
          <MicArcSchematic activeSerials={activeSerials} />
        </aside>
      </div>
      <div className="flex items-center justify-between gap-3 flex-wrap text-[11px] text-gray-500 px-1">
        <span>
          Zoom: scroll over the plot, or drag along the radial axis. Revert: double-click the plot
          or press Reset view.
        </span>
        <button
          type="button"
          onClick={() => setResetKey((k) => k + 1)}
          className="text-xs px-2 py-1 rounded border border-gray-600 text-gray-300 hover:bg-gray-700 hover:text-white"
        >
          ⟲ Reset view
        </button>
      </div>
    </div>
  );
}
