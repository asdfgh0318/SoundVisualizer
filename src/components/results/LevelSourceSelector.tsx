import type { FFTResponse } from '../../api/types';
import { type LevelSource, medianOf } from './levelSource';

interface Props {
  source: LevelSource;
  onChange: (s: LevelSource) => void;
  ffts: FFTResponse[];
}

export function LevelSourceSelector({ source, onChange, ffts }: Props) {
  const bpfs = ffts.map((f) => f.bpf_hz).filter((b): b is number => b != null);
  const bpf = bpfs.length ? medianOf(bpfs) : null;
  const noTone = ffts.length > 0 && bpfs.length === 0;
  const options: { key: string; label: string; value: LevelSource }[] = [
    { key: 'band', label: 'Mixed band', value: { kind: 'band' } },
    { key: 'broadband', label: 'Broadband (tones notched)', value: { kind: 'broadband' } },
    ...[1, 2, 3, 4].map((h) => ({ key: `tone${h}`, label: `BPF ×${h}`, value: { kind: 'tone', harmonic: h } as LevelSource })),
  ];
  const activeKey = source.kind === 'tone' ? `tone${source.harmonic}` : source.kind;
  return (
    <div className="flex items-center gap-3 flex-wrap text-xs">
      <div className="flex bg-gray-800 border border-gray-700 rounded-md overflow-hidden">
        {options.map((o) => (
          <button
            key={o.key}
            type="button"
            onClick={() => onChange(o.value)}
            disabled={o.value.kind === 'tone' && noTone}
            className={`px-3 py-1.5 font-medium transition-colors disabled:opacity-40 ${
              activeKey === o.key ? 'bg-indigo-600 text-white' : 'text-gray-300 hover:bg-gray-700'
            }`}
          >
            {o.label}
          </button>
        ))}
      </div>
      <span className="text-gray-400">
        {bpf != null
          ? <>BPF <span className="font-mono text-gray-200">{bpf.toFixed(1)} Hz</span> (from the audio)</>
          : noTone ? 'no blade-passage tone found in these captures' : ''}
      </span>
      {source.kind === 'tone' && (
        <span className="text-amber-400">
          A tone samples the room at one frequency; below ~1 kHz it can be off by several dB (see docs/arc-validation-remedies.pdf).
        </span>
      )}
    </div>
  );
}

