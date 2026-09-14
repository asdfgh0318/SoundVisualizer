/** Which September 2026 horizontal-arc captures were taken with the arc turned 180°.
 *
 * Not derivable from the stored data: the orientation was never recorded at capture
 * time, and `detect_rotated()` in `scripts/arc_error_map.py` recovered it afterwards by
 * testing which labelling makes the twelve runs agree. Its verdict is in the data pack
 * `docs/analysis/arc-validation-data.json` (`runs[*].flipped`) and is repeated here so
 * the UI can warn before anyone overlays a flipped capture on an unflipped one, where
 * every elevation label is mirrored.
 *
 * prop1–prop6 and the two 31 August captures are `UNDETERMINED`, not "upright": the
 * same fit found them incoherent with both orientations (`runs[*].coherent === false`),
 * so their labelling is unknown rather than known-good.
 */

/** Arc turned 180°, so a capture's `+e` label is physically at `−e`. */
export const FLIPPED_KEY_SLUGS: ReadonlySet<string> = new Set([
  '2004__6in__unset__dp1-baseline-horizontal-prop11',
  '2004__6in__unset__dp1-baseline-horizontal-prop12',
  '2004__6in__unset__dp1-baseline-horizontal-prop13',
  '2004__6in__unset__dp1-baseline-horizontal-prop14',
]);

/** Orientation could not be recovered — do not assume these are upright. */
export const UNDETERMINED_KEY_SLUGS: ReadonlySet<string> = new Set([
  '2004__6in__unset__dp1-baseline-horizontal-2026-08-31',
  '2004__6in__unset__dp1-baseline-horizontal-2',
  '2004__6in__unset__dp1-baseline-horizontal-3',
  '2004__6in__unset__dp1-baseline-horizontal-4',
  '2004__6in__unset__dp1-baseline-horizontal-5',
  '2004__6in__unset__dp1-baseline-horizontal-6',
  '2004__6in__unset__dp1-baseline-horizontal-prop1',
  '2004__6in__unset__dp1-baseline-horizontal-prop2',
  '2004__6in__unset__dp1-baseline-horizontal-prop3',
  '2004__6in__unset__dp1-baseline-horizontal-prop4',
  '2004__6in__unset__dp1-baseline-horizontal-prop5',
  '2004__6in__unset__dp1-baseline-horizontal-prop6',
]);

/** `F` if the arc was turned 180° for this base, `?` if the orientation is unknown. */
export function arcOrientationMark(slug: string): '' | 'F' | '?' {
  if (FLIPPED_KEY_SLUGS.has(slug)) return 'F';
  if (UNDETERMINED_KEY_SLUGS.has(slug)) return '?';
  return '';
}

export const ARC_ORIENTATION_LEGEND =
  'F = arc turned 180°, so every elevation label is mirrored. ' +
  '? = orientation could not be recovered from the data.';
