import type { FFTResponse } from '../../api/types';
import type { FreqBand } from './FrequencyBandSelector';

/**
 * What number a polar point is made of. The mixed band (default) integrates the
 * whole spectrum between the band edges, tones included — the view that hid the
 * arc-validation result. "BPF harmonic h" plots one blade-passage harmonic at its
 * own frequency, read from each capture's spectrum. "Broadband" sums the
 * tone-notched third-octaves inside the band, i.e. the room's answer to a
 * broadband source with the propeller's line spectrum removed.
 */
export type LevelSource =
  | { kind: 'band' }
  | { kind: 'tone'; harmonic: number }
  | { kind: 'broadband' };

const ONE_THIRD = Math.pow(2, 1 / 6);

export function levelForSource(fft: FFTResponse, source: LevelSource, band: FreqBand): number {
  if (source.kind === 'tone') {
    const t = fft.tones?.find((x) => x.harmonic === source.harmonic);
    return t ? t.level_db : Number.NaN;
  }
  if (source.kind === 'broadband') {
    let total = 0;
    let any = false;
    (fft.band_centres_hz ?? []).forEach((fc, i) => {
      const lvl = fft.broadband_bands_db?.[i];
      if (lvl == null) return;
      // a third-octave counts when it overlaps the selected band
      if (fc * ONE_THIRD <= band.low_hz || fc / ONE_THIRD >= band.high_hz) return;
      total += Math.pow(10, lvl / 10);
      any = true;
    });
    return any ? 10 * Math.log10(total) : Number.NaN;
  }
  return bandPowerDb(fft.frequencies, fft.magnitudes_db, band.low_hz, band.high_hz);
}


/** Integrate a PSD (dB/Hz) between two frequencies → level in dB. */
export function bandPowerDb(freqs: number[], magsDb: number[], low: number, high: number): number {
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

export function medianOf(xs: number[]): number {
  const s = [...xs].sort((a, b) => a - b);
  const m = Math.floor(s.length / 2);
  return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
}
