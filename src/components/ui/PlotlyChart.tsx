import Plotly from 'plotly.js-dist-min';
import { useEffect, useRef } from 'react';
import type { Data, Layout, PlotMouseEvent } from 'plotly.js';

interface Props {
  data: Data[];
  layout: Partial<Layout>;
  className?: string;
  onClick?: (event: PlotMouseEvent) => void;
}

const DEFAULT_CONFIG = { responsive: true, displayModeBar: false } as const;

interface PlotlyHTMLDiv extends HTMLDivElement {
  on?: (event: string, handler: (e: PlotMouseEvent) => void) => void;
  removeAllListeners?: (event: string) => void;
}

export function PlotlyChart({ data, layout, className, onClick }: Props) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const node = ref.current as PlotlyHTMLDiv | null;
    if (!node) return;
    Plotly.newPlot(node, data, layout, DEFAULT_CONFIG);
    if (onClick && node.on) {
      node.on('plotly_click', onClick);
    }
    return () => {
      if (node.removeAllListeners) node.removeAllListeners('plotly_click');
      Plotly.purge(node);
    };
  }, [data, layout, onClick]);

  return <div ref={ref} className={className} />;
}
