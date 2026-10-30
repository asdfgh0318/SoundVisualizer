import type { Key } from '../../api/types';
import { arcMark } from '../../content/arcOrientation';

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
  const span = keyDays(k);
  if (span) parts.push(span);
  const mark = arcMark(k);
  return parts.join(' · ') + (mark ? `  [${mark}]` : '');
}

/** Local calendar day (YYYY-MM-DD) of an ISO timestamp, the same day the day overlay uses. */
export const localDay = (iso: string) => new Date(iso).toLocaleDateString('sv');

/** The days a base was captured on, so repeats of the same material on different days are
 *  told apart: "2026-10-28", or "2026-10-28…2026-10-30" when it spans several. */
export function keyDays(k: Key): string {
  if (!k.first_measured_at || !k.last_measured_at) return '';
  const a = localDay(k.first_measured_at);
  const b = localDay(k.last_measured_at);
  return a === b ? a : `${a}…${b}`;
}

/** Days of the captures behind one series point, in the same form as `keyDays`. */
export function captureDays(tStarts: string[]): string {
  const days = [...new Set(tStarts.map(localDay))].sort();
  if (!days.length) return '';
  return days.length === 1 ? days[0] : `${days[0]}…${days.at(-1)}`;
}

/** Shorter form for chart legends and series chips, where the motor is the same for
 *  every series on screen and the notes are what the reader is actually comparing. */
export function seriesLabel(k: Key): string {
  const parts = [k.propeller];
  if (k.shroud && k.shroud !== 'none') parts.push(k.shroud);
  if (k.notes && k.notes !== 'unset') parts.push(k.notes);
  const mark = arcMark(k);
  return (parts.join(' · ') || k.motor) + (mark ? `  [${mark}]` : '');
}
