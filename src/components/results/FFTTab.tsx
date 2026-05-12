import { useState } from 'react';
import type { FFTSettings, PWMPoint } from '../../api/types';
import { FFTRow } from './FFTRow';
import { FFTSettingsBar } from './FFTSettingsPopover';

interface Props {
  keySlug: string;
  point: PWMPoint;
}

const DEFAULT_SETTINGS: FFTSettings = { window: 'hann', size: 4096, overlap: 0.5 };

export function FFTTab({ keySlug, point }: Props) {
  const [settings, setSettings] = useState<FFTSettings>(DEFAULT_SETTINGS);

  return (
    <div className="space-y-4">
      <FFTSettingsBar settings={settings} onChange={setSettings} />
      <div className="space-y-3">
        {point.acoustic.length === 0 && (
          <div className="text-sm text-gray-400 italic">
            No acoustic measurements at this PWM point.
          </div>
        )}
        {point.acoustic.map((a) => (
          <FFTRow key={a.id} keySlug={keySlug} acoustic={a} settings={settings} />
        ))}
      </div>
    </div>
  );
}
