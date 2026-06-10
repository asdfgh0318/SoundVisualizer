import type { Data, Layout } from 'plotly.js';
import { useMemo } from 'react';
import { PlotlyChart } from '../ui/PlotlyChart';

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
}

const GRID = '#374151';
const TEXT = '#9ca3af';

const HOVER =
  '%{fullData.name}<br>elev %{customdata[0]}° (%{customdata[1]})<br>%{r:.1f} dB<extra></extra>';

// Plotly default polar convention: theta=0 is at 3 o'clock (right), increases
// counter-clockwise. We want elevation = +90° at 12 o'clock, 0° at 3 o'clock,
// -90° at 6 o'clock. Negative elevations wrap below: -45 → 315, -90 → 270.
const elevToTheta = (e: number): number => (e >= 0 ? e : 360 + e);
// Mirror across the vertical axis (the 12-6 line): θ_mirror = 180 - θ_right.
const elevToMirrorTheta = (e: number): number => 180 - e;

export function PolarPolarPlot({ series, rangeMode }: Props) {
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
        hovertemplate: HOVER,
        name: s.label,
      };

      traces.push({ ...base, theta: elevs.map(elevToTheta), r: spls, customdata: cd, showlegend: showLegend });

      if (rangeMode === 360) {
        // Mirror trace shares the legend entry → don't double-list it.
        traces.push({ ...base, theta: elevs.map(elevToMirrorTheta), r: spls, customdata: cd, showlegend: false });
      }
    }
    return traces;
  }, [series, rangeMode, showLegend]);

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
          ticksuffix: ' dB',
          angle: 0,
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
  }, [rangeMode, showLegend]);

  return <PlotlyChart data={data} layout={layout} className="w-full" />;
}
