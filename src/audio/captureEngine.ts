import type { MicAssignment, AudioCapture, TriggerConfig } from '../types/index.ts';
import { alignCaptures } from './triggerSync.ts';

const PROCESSOR_URL = new URL('./recorderProcessor.ts', import.meta.url).href;

let audioContext: AudioContext | null = null;
let workletLoaded = false;

async function getAudioContext(sampleRate: number): Promise<AudioContext> {
  if (audioContext && audioContext.sampleRate === sampleRate) {
    if (audioContext.state === 'suspended') {
      await audioContext.resume();
    }
    return audioContext;
  }
  if (audioContext) {
    await audioContext.close();
  }
  audioContext = new AudioContext({ sampleRate });
  workletLoaded = false;
  return audioContext;
}

async function ensureWorklet(ctx: AudioContext): Promise<void> {
  if (workletLoaded) return;
  await ctx.audioWorklet.addModule(PROCESSOR_URL);
  workletLoaded = true;
}

interface CaptureHandle {
  stream: MediaStream;
  source: MediaStreamAudioSourceNode;
  workletNode: AudioWorkletNode;
  promise: Promise<Float32Array>;
}

function createCaptureHandle(
  ctx: AudioContext,
  stream: MediaStream,
  durationSec: number,
  onProgress: (percent: number) => void,
): CaptureHandle {
  const source = ctx.createMediaStreamSource(stream);
  const workletNode = new AudioWorkletNode(ctx, 'recorder-processor');

  const promise = new Promise<Float32Array>((resolve, reject) => {
    workletNode.port.onmessage = (e: MessageEvent) => {
      if (e.data.type === 'progress') {
        onProgress(e.data.percent);
      } else if (e.data.type === 'complete') {
        resolve(e.data.samples as Float32Array);
      }
    };
    workletNode.onprocessorerror = () => {
      reject(new Error('AudioWorklet processor error'));
    };
  });

  source.connect(workletNode);
  // Don't connect to destination — we don't want playback
  workletNode.connect(ctx.destination);

  // Start recording
  workletNode.port.postMessage({
    command: 'start',
    durationSec,
    sampleRate: ctx.sampleRate,
  });

  return { stream, source, workletNode, promise };
}

function cleanupHandle(handle: CaptureHandle): void {
  handle.source.disconnect();
  handle.workletNode.disconnect();
  handle.stream.getTracks().forEach((t) => t.stop());
}

export async function captureAllMics(
  assignments: MicAssignment[],
  durationSec: number,
  sampleRate: number,
  onProgress: (percent: number) => void,
  triggerConfig?: TriggerConfig,
): Promise<AudioCapture[]> {
  const ctx = await getAudioContext(sampleRate);
  await ensureWorklet(ctx);

  const activeAssignments = assignments.filter((a) => a.deviceId !== '');
  if (activeAssignments.length === 0) {
    throw new Error('No microphones assigned');
  }

  // Get streams for all assigned mics
  const streams = await Promise.all(
    activeAssignments.map((a) =>
      navigator.mediaDevices.getUserMedia({
        audio: {
          deviceId: { exact: a.deviceId },
          sampleRate: { ideal: sampleRate },
          echoCancellation: false,
          noiseSuppression: false,
          autoGainControl: false,
        },
      }),
    ),
  );

  // Per-mic progress tracking
  const progressPerMic = new Array(activeAssignments.length).fill(0);

  const handles = streams.map((stream, i) =>
    createCaptureHandle(ctx, stream, durationSec, (pct) => {
      progressPerMic[i] = pct;
      const avg = progressPerMic.reduce((s, v) => s + v, 0) / progressPerMic.length;
      onProgress(Math.floor(avg));
    }),
  );

  try {
    const results = await Promise.all(handles.map((h) => h.promise));

    let captures = activeAssignments.map((assignment, i) => ({
      elevationDeg: assignment.elevationDeg,
      deviceId: assignment.deviceId,
      audioData: results[i],
      sampleRate: ctx.sampleRate,
      durationSec,
    }));

    // Apply trigger-based synchronization if configured
    if (triggerConfig?.enabled) {
      captures = alignCaptures(captures, triggerConfig);
    }

    return captures;
  } finally {
    handles.forEach(cleanupHandle);
  }
}

export function closeAudioContext(): void {
  if (audioContext) {
    audioContext.close();
    audioContext = null;
    workletLoaded = false;
  }
}
