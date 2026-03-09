import type { SplResult, DirectivityMetrics } from '../types/index.ts';

/**
 * Approximate CEA-2034 (spinorama) broadband directivity metrics from a sparse
 * measurement grid of 5 elevation angles and N azimuth positions.
 *
 * A full CEA-2034 measurement requires 70 positions (10° increments, both
 * horizontal and vertical planes) and frequency-dependent SPL data. With only
 * 5 elevation angles (-90°, -45°, 0°, +45°, +90°) and broadband SPL, we
 * compute approximate equivalents using solid-angle weighting.
 *
 * Based on methodology from:
 * - Audiomatica AN-022: Creating Spinorama Plots from Polar Measurement Sets
 * - pierreaubert/spinorama (GitHub): CEA-2034 computation algorithms
 * - Klippel AN 54/69: Directivity measurement with turntables and mic arrays
 *
 * Solid angle weighting: Each measurement point represents a band on the sphere.
 * The weight is proportional to cos(elevation) — points near the equator cover
 * more solid angle than points near the poles.
 */

/**
 * Solid-angle weight for an elevation band centered at elevDeg.
 * Uses cos(elevation) as the integration weight for spherical surface area.
 * The 45° bands span ±22.5° each; poles span the remaining caps.
 */
function elevationWeight(elevDeg: number): number {
  // Band boundaries (halfway between measurement elevations)
  // -90: [-90, -67.5]   -> sin(-67.5) - sin(-90)
  // -45: [-67.5, -22.5] -> sin(-22.5) - sin(-67.5)
  //   0: [-22.5, +22.5] -> sin(+22.5) - sin(-22.5)
  // +45: [+22.5, +67.5] -> sin(+67.5) - sin(+22.5)
  // +90: [+67.5, +90]   -> sin(+90)   - sin(+67.5)
  const bandMap = new Map<number, [number, number]>([
    [-90, [-90, -67.5]],
    [-45, [-67.5, -22.5]],
    [0, [-22.5, 22.5]],
    [45, [22.5, 67.5]],
    [90, [67.5, 90]],
  ]);

  const band = bandMap.get(elevDeg);
  if (!band) return 0;

  const [lo, hi] = band;
  const toRad = Math.PI / 180;
  return Math.sin(hi * toRad) - Math.sin(lo * toRad);
}

/**
 * Average SPL values in dB using energy (power) averaging.
 * SPL_avg = 10 * log10( mean( 10^(SPL_i/10) ) )
 */
function energyAverageDb(values: number[]): number {
  if (values.length === 0) return -Infinity;
  const finite = values.filter((v) => isFinite(v));
  if (finite.length === 0) return -Infinity;
  const mean = finite.reduce((s, v) => s + Math.pow(10, v / 10), 0) / finite.length;
  return 10 * Math.log10(mean);
}

/**
 * Weighted energy average in dB using solid-angle weights.
 */
function weightedEnergyAverageDb(
  values: { splDb: number; weight: number }[],
): number {
  const finite = values.filter((v) => isFinite(v.splDb) && v.weight > 0);
  if (finite.length === 0) return -Infinity;
  const totalWeight = finite.reduce((s, v) => s + v.weight, 0);
  const weightedSum = finite.reduce(
    (s, v) => s + v.weight * Math.pow(10, v.splDb / 10),
    0,
  );
  return 10 * Math.log10(weightedSum / totalWeight);
}

/**
 * Compute approximate CEA-2034 broadband directivity metrics.
 *
 * @param data - All SPL results from measurements.
 * @returns DirectivityMetrics or null if insufficient data.
 */
export function computeDirectivityMetrics(
  data: SplResult[],
): DirectivityMetrics | null {
  if (data.length === 0) return null;

  const finite = data.filter((d) => isFinite(d.splDb));
  if (finite.length === 0) return null;

  // --- On-Axis ---
  // Best: elevation=0, azimuth=0. Fallback: closest to on-axis.
  const onAxis = finite.find(
    (d) => d.elevationDeg === 0 && d.azimuthDeg === 0,
  );
  const onAxisDb = onAxis
    ? onAxis.splDb
    : energyAverageDb(
        finite.filter((d) => d.elevationDeg === 0).map((d) => d.splDb),
      );

  // --- Listening Window ---
  // CEA-2034: ±30° horizontal, ±10° vertical.
  // With our grid (0°, ±45° elevation), only elevation=0 falls within ±10°.
  // Horizontal: 0°, ±10°, ±20°, ±30° — we use whatever azimuth positions fall within ±30°.
  const lwData = finite.filter(
    (d) =>
      d.elevationDeg === 0 &&
      (d.azimuthDeg <= 30 || d.azimuthDeg >= 330),
  );
  const listeningWindowDb =
    lwData.length > 0 ? energyAverageDb(lwData.map((d) => d.splDb)) : onAxisDb;

  // --- Sound Power ---
  // Solid-angle-weighted average across ALL measurement positions.
  // Group by elevation, compute per-elevation energy average, then weight.
  const elevations = [-90, -45, 0, 45, 90];
  const perElevAvg = elevations.map((elev) => {
    const elevData = finite.filter((d) => d.elevationDeg === elev);
    return {
      splDb: energyAverageDb(elevData.map((d) => d.splDb)),
      weight: elevationWeight(elev),
    };
  });
  const soundPowerDb = weightedEnergyAverageDb(perElevAvg);

  // --- Directivity Index ---
  const directivityIndexDb = isFinite(onAxisDb) && isFinite(soundPowerDb)
    ? onAxisDb - soundPowerDb
    : 0;

  // --- Early Reflections (approximate) ---
  // CEA-2034 defines ER from specific wall reflection groups.
  // We approximate: floor (elev=-45 to -90), ceiling (elev=+45 to +90),
  // front wall (az=0±30, elev=0), side walls (az=60-120 & 240-300, elev=0),
  // rear wall (az=150-210, elev=0).
  const erGroups: number[][] = [];

  // Floor bounce: -45° and -90° elevation
  const floorData = finite
    .filter((d) => d.elevationDeg === -45 || d.elevationDeg === -90)
    .map((d) => d.splDb);
  if (floorData.length > 0) erGroups.push(floorData);

  // Ceiling bounce: +45° and +90° elevation
  const ceilData = finite
    .filter((d) => d.elevationDeg === 45 || d.elevationDeg === 90)
    .map((d) => d.splDb);
  if (ceilData.length > 0) erGroups.push(ceilData);

  // Front wall: elev=0, az within ±30°
  const frontData = finite
    .filter(
      (d) =>
        d.elevationDeg === 0 &&
        (d.azimuthDeg <= 30 || d.azimuthDeg >= 330),
    )
    .map((d) => d.splDb);
  if (frontData.length > 0) erGroups.push(frontData);

  // Side walls: elev=0, az 60-120° and 240-300°
  const sideData = finite
    .filter(
      (d) =>
        d.elevationDeg === 0 &&
        ((d.azimuthDeg >= 60 && d.azimuthDeg <= 120) ||
          (d.azimuthDeg >= 240 && d.azimuthDeg <= 300)),
    )
    .map((d) => d.splDb);
  if (sideData.length > 0) erGroups.push(sideData);

  // Rear wall: elev=0, az 150-210°
  const rearData = finite
    .filter(
      (d) =>
        d.elevationDeg === 0 &&
        d.azimuthDeg >= 150 &&
        d.azimuthDeg <= 210,
    )
    .map((d) => d.splDb);
  if (rearData.length > 0) erGroups.push(rearData);

  // Average across groups (each group equally weighted)
  const earlyReflectionsDb =
    erGroups.length > 0
      ? energyAverageDb(erGroups.map((g) => energyAverageDb(g)))
      : soundPowerDb;

  return {
    onAxisDb,
    listeningWindowDb,
    soundPowerDb,
    directivityIndexDb,
    earlyReflectionsDb,
    measurementCount: finite.length,
  };
}
