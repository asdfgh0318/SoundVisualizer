/**
 * Radix-2 Cooley-Tukey FFT — ported from HoloLaser.
 * Operates on separate real/imaginary Float64Arrays in-place.
 */

export function fft(re: Float64Array, im: Float64Array): void {
  const n = re.length;
  if (n <= 1) return;
  if ((n & (n - 1)) !== 0) {
    throw new Error(`FFT length must be a power of 2, got ${n}`);
  }

  bitReverse(re, im, n);

  for (let size = 2; size <= n; size *= 2) {
    const halfSize = size / 2;
    const angleStep = (-2 * Math.PI) / size;
    const wRe = Math.cos(angleStep);
    const wIm = Math.sin(angleStep);

    for (let i = 0; i < n; i += size) {
      let curRe = 1;
      let curIm = 0;

      for (let j = 0; j < halfSize; j++) {
        const evenIdx = i + j;
        const oddIdx = i + j + halfSize;

        const tRe = curRe * re[oddIdx] - curIm * im[oddIdx];
        const tIm = curRe * im[oddIdx] + curIm * re[oddIdx];

        re[oddIdx] = re[evenIdx] - tRe;
        im[oddIdx] = im[evenIdx] - tIm;
        re[evenIdx] = re[evenIdx] + tRe;
        im[evenIdx] = im[evenIdx] + tIm;

        const newCurRe = curRe * wRe - curIm * wIm;
        const newCurIm = curRe * wIm + curIm * wRe;
        curRe = newCurRe;
        curIm = newCurIm;
      }
    }
  }
}

function bitReverse(re: Float64Array, im: Float64Array, n: number): void {
  let j = 0;
  for (let i = 0; i < n - 1; i++) {
    if (i < j) {
      const tmpRe = re[i];
      re[i] = re[j];
      re[j] = tmpRe;
      const tmpIm = im[i];
      im[i] = im[j];
      im[j] = tmpIm;
    }
    let k = n >> 1;
    while (k <= j) {
      j -= k;
      k >>= 1;
    }
    j += k;
  }
}

export function nextPow2(n: number): number {
  let p = 1;
  while (p < n) p <<= 1;
  return p;
}
