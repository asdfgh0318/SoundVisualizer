/**
 * AudioWorklet processor that records raw Float32 samples into a buffer.
 * Runs on the audio rendering thread.
 *
 * Messages IN:  { command: 'start', durationSec: number, sampleRate: number }
 *               { command: 'stop' }
 * Messages OUT: { type: 'progress', percent: number }
 *               { type: 'complete', samples: Float32Array }
 */

class RecorderProcessor extends AudioWorkletProcessor {
  private buffer: Float32Array | null = null;
  private writeIndex = 0;
  private totalSamples = 0;
  private recording = false;
  private lastProgressPct = -1;

  constructor() {
    super();
    this.port.onmessage = (e: MessageEvent) => {
      const { command, durationSec, sampleRate } = e.data;
      if (command === 'start') {
        this.totalSamples = Math.ceil(durationSec * sampleRate);
        this.buffer = new Float32Array(this.totalSamples);
        this.writeIndex = 0;
        this.recording = true;
        this.lastProgressPct = -1;
      } else if (command === 'stop') {
        this.finalize();
      }
    };
  }

  process(inputs: Float32Array[][]): boolean {
    if (!this.recording || !this.buffer) return true;

    const input = inputs[0];
    if (!input || input.length === 0) return true;

    const channel = input[0];
    const remaining = this.totalSamples - this.writeIndex;
    const toCopy = Math.min(channel.length, remaining);

    this.buffer.set(channel.subarray(0, toCopy), this.writeIndex);
    this.writeIndex += toCopy;

    // Report progress every ~1%
    const pct = Math.floor((this.writeIndex / this.totalSamples) * 100);
    if (pct !== this.lastProgressPct) {
      this.lastProgressPct = pct;
      this.port.postMessage({ type: 'progress', percent: pct });
    }

    if (this.writeIndex >= this.totalSamples) {
      this.finalize();
    }

    return true;
  }

  private finalize(): void {
    this.recording = false;
    if (this.buffer) {
      // Transfer the buffer to the main thread
      const samples = this.buffer.slice(0, this.writeIndex);
      this.port.postMessage({ type: 'complete', samples }, [samples.buffer]);
      this.buffer = null;
    }
  }
}

registerProcessor('recorder-processor', RecorderProcessor);
