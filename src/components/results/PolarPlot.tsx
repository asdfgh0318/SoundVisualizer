import type { Data, Layout } from 'plotly.js';
import { useMemo } from 'react';
import { PlotlyChart } from '../ui/PlotlyChart';

export interface PolarPoint {
  elevation_deg: number;
  spl_db: number;
  mic_serial: string;
}

interface Props {
  /** Sorted by elevation descending (+90 → -90). */
  points: PolarPoint[];
  rangeMode: 180 | 360;
}

const COLOR = '#818cf8';
const GRID = '#374151';
const TEXT = '#9ca3af';

const HOVER =
  'elev %{customdata[0]}° (%{customdata[1]})<br>%{r:.1f} dB<extra></extra>';

const TRACE_DEFAULTS = {
  type: 'scatterpolar' as const,
  mode: 'lines+markers' as const,
  line: { color: COLOR, width: 2 },
  marker: { color: COLOR, size: 7 },
  hovertemplate: HOVER,
  showlegend: false,
};

// Plotly default polar convention: theta=0 is at 3 o'clock (right), increases
// counter-clockwise. We want elevation = +90° at 12 o'clock, 0° at 3 o'clock,
// -90° at 6 o'clock. Map: elev → polar_theta in [0, 360) running counter-clockwise
// from the +x axis. Negative elevations wrap below: -45 → 315, -90 → 270.
const elevToTheta = (e: number): number => (e >= 0 ? e : 360 + e);
// Mirror across the vertical axis (the 12-6 line): θ_mirror = 180 - θ_right.
const elevToMirrorTheta = (e: number): number => 180 - e;

export function PolarPolarPlot({ points, rangeMode }: Props) {
  const data = useMemo<Data[]>(() => {
    if (points.length < 2) return [];

    const elevs = points.map((p) => p.elevation_deg);
    const spls = points.map((p) => p.spl_db);
    const serials = points.map((p) => p.mic_serial);
    const cd = elevs.map((e, i): [number, string] => [e, serials[i]]);

    const rightTrace: Data = {
      ...TRACE_DEFAULTS,
      theta: elevs.map(elevToTheta),
      r: spls,
      customdata: cd,
    };

    if (rangeMode === 180) return [rightTrace];

    const leftTrace: Data = {
      ...TRACE_DEFAULTS,
      theta: elevs.map(elevToMirrorTheta),
      r: spls,
      customdata: cd,
    };
    return [rightTrace, leftTrace];
  }, [points, rangeMode]);

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
          // anchor the radial axis on the right side so labels are out of the way
          angle: 0,
        },
        angularaxis: {
          // standard math convention: theta=0 at 3 o'clock, counter-clockwise.
          tickmode: 'array',
          tickvals: rangeMode === 360 ? ticks360 : ticks180,
          ticktext: rangeMode === 360 ? labels360 : labels180,
          gridcolor: GRID,
          linecolor: GRID,
          tickfont: { color: TEXT, size: 11 },
        },
        // 180° mode → right half of circle (CSS sector [270, 90] wraps through 0).
        // 360° mode → full circle.
        sector: rangeMode === 180 ? [270, 450] : [0, 360],
      },
      margin: { l: 40, r: 40, t: 30, b: 30 },
      showlegend: false,
    };
  }, [rangeMode]);

  return <PlotlyChart data={data} layout={layout} className="w-full" />;
}
