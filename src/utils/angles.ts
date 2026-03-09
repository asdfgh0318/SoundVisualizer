/**
 * Format elevation angle with sign and degree symbol.
 */
export function formatElevation(deg: number): string {
  if (deg > 0) return `+${deg}\u00b0`;
  if (deg < 0) return `${deg}\u00b0`;
  return `0\u00b0`;
}

/**
 * Format azimuth angle with degree symbol.
 */
export function formatAzimuth(deg: number): string {
  return `${deg}\u00b0`;
}

/**
 * Normalize an angle to [0, 360).
 */
export function normalizeAzimuth(deg: number): number {
  return ((deg % 360) + 360) % 360;
}
