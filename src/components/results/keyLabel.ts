import type { Key } from '../../api/types';
import { arcOrientationMark } from '../../content/arcOrientation';

/** One place both base pickers get their option text from.
 *
 * They used to build it independently and drifted: the overlay picker dropped the
 * notes, which is the only field that separates twenty-odd captures of the same motor
 * and propeller, so every horizontal-arc base rendered as "2004 · 6in".
 */
export function keyLabel(k: Key): string {
  const parts = [k.motor, k.propeller];
  if (k.shroud && k.shroud !== 'none') parts.push(k.shroud);
  if (k.notes && k.notes !== 'unset') parts.push(k.notes);
  const mark = arcOrientationMark(k.slug);
  return parts.join(' · ') + (mark ? `  ${mark}` : '');
}

/** Shorter form for chart legends and series chips, where the motor is the same for
 *  every series on screen and the notes are what the reader is actually comparing. */
export function seriesLabel(k: Key): string {
  const parts = [k.propeller];
  if (k.shroud && k.shroud !== 'none') parts.push(k.shroud);
  if (k.notes && k.notes !== 'unset') parts.push(k.notes);
  const mark = arcOrientationMark(k.slug);
  return (parts.join(' · ') || k.motor) + (mark ? `  ${mark}` : '');
}
