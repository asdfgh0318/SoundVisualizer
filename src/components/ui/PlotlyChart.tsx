import Plotly from 'plotly.js-dist-min';
import { useEffect, useRef } from 'react';
import type { Config, Data, Layout, PlotMouseEvent } from 'plotly.js';

interface Props {
  data: Data[];
  layout: Partial<Layout>;
  className?: string;
  onClick?: (event: PlotMouseEvent) => void;
  config?: Partial<Config>;
  /** Snap a polar subplot's orientation back after every interaction. */
  pinPolarOrientation?: boolean;
}

const DEFAULT_CONFIG = { responsive: true, displayModeBar: false } as const;

interface PlotlyHTMLDiv extends HTMLDivElement {
  on?: (event: string, handler: (e: PlotMouseEvent) => void) => void;
  removeAllListeners?: (event: string) => void;
  _fullLayout?: { polar?: { radialaxis?: { angle?: number }; angularaxis?: { rotation?: number } } };
}

/** Plotly lets a drag on the polar rim rotate the whole subplot, and a drag on
 *  the radial axis swing that axis to a new angle. Either one silently breaks
 *  the plot's meaning for us: elevation is pinned to the clock face (+90° up,
 *  0° right) and the radial tick labels render upside down once the axis passes
 *  the vertical. Radial-range zoom is left alone — only the orientation is held. */
function pinOrientation(node: PlotlyHTMLDiv) {
  if (!node.on) return;
  let fixing = false;
  node.on('plotly_relayout', () => {
    if (fixing) return;
    const polar = node._fullLayout?.polar;
    if (!polar) return;
    if (polar.radialaxis?.angle === 0 && polar.angularaxis?.rotation === 0) return;
    fixing = true;
    // Dotted paths are how Plotly addresses nested layout attributes; its
    // TypeScript Layout type only describes the nested form.
    const upright = {
      'polar.radialaxis.angle': 0,
      'polar.angularaxis.rotation': 0,
    } as unknown as Partial<Layout>;
    void Plotly.relayout(node, upright).then(() => {
      fixing = false;
    });
  });
}

export function PlotlyChart({ data, layout, className, onClick, config, pinPolarOrientation }: Props) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const node = ref.current as PlotlyHTMLDiv | null;
    if (!node) return;
    Plotly.newPlot(node, data, layout, { ...DEFAULT_CONFIG, ...config });
    if (onClick && node.on) {
      node.on('plotly_click', onClick);
    }
    if (pinPolarOrientation) pinOrientation(node);
    return () => {
      if (node.removeAllListeners) {
        node.removeAllListeners('plotly_click');
        node.removeAllListeners('plotly_relayout');
      }
      Plotly.purge(node);
    };
  }, [data, layout, onClick, config, pinPolarOrientation]);

  return <div ref={ref} className={className} />;
}
