import type { Key } from '../api/types';

/** How the arc was standing for a given base: normal, or laid flat and possibly turned.
 *
 * The September 2026 validation captures were taken with the arc **laid flat**, propeller
 * axis vertical, so all eleven microphones sit at one height around the axis and an
 * axisymmetric source must read the same everywhere. That is a different rig geometry
 * from every other capture in the store, where the arc stands in its normal orientation
 * and the microphones really are at different elevations. Nothing in the capture path
 * records which it was, so the flat-arc campaign is recognised by `horizontal` in the
 * base's notes.
 *
 * Within the flat campaign the arc was also turned 180° for four runs, which mirrors every
 * elevation label: a capture's `+e` is physically at `−e`. That was never recorded either;
 * `detect_rotated()` in `scripts/arc_error_map.py` recovered it afterwards by testing which
 * labelling makes the twelve coherent runs agree, and its verdict is in the data pack
 * `docs/analysis/arc-validation-data.json` as `runs[*].flipped`.
 *
 * Only those twelve runs have a recovered orientation. Every other flat-arc capture is
 * unknown, not "the reference one" — the same fit found prop1–prop6 and the two 31 August
 * captures incoherent with both orientations (`runs[*].coherent === false`). Listing the
 * confirmed ones rather than the unknown ones is deliberate: a flat-arc capture added later
 * then reads as unknown by default instead of silently looking confirmed.
 */

/** Flat-arc runs confirmed to be in the reference orientation. */
const FLAT_REFERENCE = new Set([
  'dp1-baseline-horizontal-prop7',
  'dp1-baseline-horizontal-prop8',
  'dp1-baseline-horizontal-prop9',
  'dp1-baseline-horizontal-prop10',
  'dp1-baseline-horizontal-prop15',
  'dp1-baseline-horizontal-prop16',
  'dp1-baseline-horizontal-prop17',
  'dp1-baseline-horizontal-prop18',
]);

/** Flat-arc runs confirmed to have been turned 180°, so the elevation labels are mirrored. */
const FLAT_TURNED = new Set([
  'dp1-baseline-horizontal-prop11',
  'dp1-baseline-horizontal-prop12',
  'dp1-baseline-horizontal-prop13',
  'dp1-baseline-horizontal-prop14',
]);

export type ArcState = 'normal' | 'flat' | 'flat-turned' | 'flat-unknown';

export function arcState(k: Key): ArcState {
  if (!/horizontal/i.test(k.notes)) return 'normal';
  if (FLAT_TURNED.has(k.notes)) return 'flat-turned';
  if (FLAT_REFERENCE.has(k.notes)) return 'flat';
  return 'flat-unknown';
}

/** Short mark for a base picker: `H` flat, `H F` flat and turned, `H ?` flat and unknown. */
export function arcMark(k: Key): string {
  switch (arcState(k)) {
    case 'flat-turned':
      return 'H F';
    case 'flat-unknown':
      return 'H ?';
    case 'flat':
      return 'H';
    default:
      return '';
  }
}

export const ARC_ORIENTATION_LEGEND =
  'H = arc laid flat for the validation campaign, not in its normal orientation. ' +
  'H F = laid flat and turned 180°, so every elevation label is mirrored. ' +
  'H ? = laid flat, but which of the two orientations was never recovered. ' +
  'Unmarked bases were captured with the arc standing normally.';
