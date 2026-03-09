/**
 * Encode a Float32Array of audio samples into a WAV file blob.
 */

export function encodeWav(
  samples: Float32Array,
  sampleRate: number,
  bitDepth: 16 | 32 = 16,
): Blob {
  const numChannels = 1;
  const bytesPerSample = bitDepth / 8;
  const dataLength = samples.length * bytesPerSample;
  const headerLength = 44;
  const totalLength = headerLength + dataLength;

  const buffer = new ArrayBuffer(totalLength);
  const view = new DataView(buffer);

  // RIFF header
  writeString(view, 0, 'RIFF');
  view.setUint32(4, totalLength - 8, true);
  writeString(view, 8, 'WAVE');

  // fmt chunk
  writeString(view, 12, 'fmt ');
  view.setUint32(16, 16, true); // chunk size
  view.setUint16(20, bitDepth === 32 ? 3 : 1, true); // format: 3=float, 1=PCM
  view.setUint16(22, numChannels, true);
  view.setUint32(24, sampleRate, true);
  view.setUint32(28, sampleRate * numChannels * bytesPerSample, true); // byte rate
  view.setUint16(32, numChannels * bytesPerSample, true); // block align
  view.setUint16(34, bitDepth, true);

  // data chunk
  writeString(view, 36, 'data');
  view.setUint32(40, dataLength, true);

  // Write samples
  if (bitDepth === 32) {
    for (let i = 0; i < samples.length; i++) {
      view.setFloat32(headerLength + i * 4, samples[i], true);
    }
  } else {
    for (let i = 0; i < samples.length; i++) {
      const clamped = Math.max(-1, Math.min(1, samples[i]));
      const int16 = clamped < 0 ? clamped * 0x8000 : clamped * 0x7fff;
      view.setInt16(headerLength + i * 2, int16, true);
    }
  }

  return new Blob([buffer], { type: 'audio/wav' });
}

export function downloadWav(blob: Blob, filename: string): void {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

export function downloadCapture(
  samples: Float32Array,
  sampleRate: number,
  filename: string,
  bitDepth: 16 | 32 = 16,
): void {
  const blob = encodeWav(samples, sampleRate, bitDepth);
  downloadWav(blob, filename);
}

function writeString(view: DataView, offset: number, str: string): void {
  for (let i = 0; i < str.length; i++) {
    view.setUint8(offset + i, str.charCodeAt(i));
  }
}
