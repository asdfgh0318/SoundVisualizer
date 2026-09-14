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
 * Orientation comes from the fit where the fit could recover it, and from Adam otherwise.
 * A flat-arc capture that has neither reads as unknown rather than as the reference one,
 * which is why the confirmed sets are listed rather than the unknown ones: one added later
 * then shows as unknown instead of silently looking confirmed.
 */

/** Flat-arc runs confirmed to be in the reference orientation.
 *
 * prop1–prop6 are here on Adam's own account of the session (2026-09-14), not on the
 * fit's: `detect_rotated()` could place only the twelve coherent runs, and it found
 * prop1–prop6 consistent with neither orientation. Whoever ran the rig outranks a fit
 * that cannot see the room. What it leaves behind is an open question rather than a
 * settled one — if the arc was standing the same way, something *else* differed in that
 * morning session (prop1 11:55 to prop6 13:13, then a three-and-a-half hour gap before
 * prop7 at 16:42), and we do not know what. They stay out of the maps until we do.
 */
const FLAT_REFERENCE = new Set([
  'dp1-baseline-horizontal-prop1',
  'dp1-baseline-horizontal-prop2',
  'dp1-baseline-horizontal-prop3',
  'dp1-baseline-horizontal-prop4',
  'dp1-baseline-horizontal-prop5',
  'dp1-baseline-horizontal-prop6',
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
