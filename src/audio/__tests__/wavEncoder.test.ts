import { describe, it, expect } from 'vitest';
import { encodeWav } from '../wavEncoder.ts';

describe('WAV Encoder', () => {
  it('produces a valid WAV header for 16-bit', async () => {
    const samples = new Float32Array([0, 0.5, -0.5, 1, -1]);
    const blob = encodeWav(samples, 48000, 16);
    const buffer = await blob.arrayBuffer();
    const view = new DataView(buffer);

    // RIFF header
    expect(String.fromCharCode(view.getUint8(0), view.getUint8(1), view.getUint8(2), view.getUint8(3))).toBe('RIFF');
    // WAVE
    expect(String.fromCharCode(view.getUint8(8), view.getUint8(9), view.getUint8(10), view.getUint8(11))).toBe('WAVE');
    // fmt
    expect(String.fromCharCode(view.getUint8(12), view.getUint8(13), view.getUint8(14), view.getUint8(15))).toBe('fmt ');
    // PCM format = 1
    expect(view.getUint16(20, true)).toBe(1);
    // 1 channel
    expect(view.getUint16(22, true)).toBe(1);
    // 48000 Hz
    expect(view.getUint32(24, true)).toBe(48000);
    // 16 bits per sample
    expect(view.getUint16(34, true)).toBe(16);
    // data chunk size = 5 samples * 2 bytes
    expect(view.getUint32(40, true)).toBe(10);
    // Total blob size = 44 header + 10 data
    expect(buffer.byteLength).toBe(54);
  });

  it('produces a valid WAV header for 32-bit float', async () => {
    const samples = new Float32Array([0, 0.5, -0.5]);
    const blob = encodeWav(samples, 44100, 32);
    const buffer = await blob.arrayBuffer();
    const view = new DataView(buffer);

    // Float format = 3
    expect(view.getUint16(20, true)).toBe(3);
    // 32 bits per sample
    expect(view.getUint16(34, true)).toBe(32);
    // data chunk size = 3 samples * 4 bytes
    expect(view.getUint32(40, true)).toBe(12);
    expect(buffer.byteLength).toBe(56);
  });

  it('correctly encodes 16-bit samples', async () => {
    const samples = new Float32Array([0, 1, -1]);
    const blob = encodeWav(samples, 48000, 16);
    const buffer = await blob.arrayBuffer();
    const view = new DataView(buffer);

    expect(view.getInt16(44, true)).toBe(0);      // silence
    expect(view.getInt16(46, true)).toBe(32767);   // max positive
    expect(view.getInt16(48, true)).toBe(-32768);  // max negative
  });

  it('correctly encodes 32-bit float samples', async () => {
    const samples = new Float32Array([0.25, -0.75]);
    const blob = encodeWav(samples, 48000, 32);
    const buffer = await blob.arrayBuffer();
    const view = new DataView(buffer);

    expect(view.getFloat32(44, true)).toBeCloseTo(0.25);
    expect(view.getFloat32(48, true)).toBeCloseTo(-0.75);
  });

  it('has correct MIME type', () => {
    const blob = encodeWav(new Float32Array(0), 48000);
    expect(blob.type).toBe('audio/wav');
  });
});
