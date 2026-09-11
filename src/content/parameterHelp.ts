/** One short explanation per user-settable parameter, shown by the ⓘ toggles. */

export const CAPTURE_HELP = {
  esc_signal:
    'Pulse width sent to the ESC at this step. 1000 µs is motor stopped, 2000 µs is full throttle. The ramp runs the steps in order and returns to 1000 µs at the end.',
  recording_ms:
    'How long every microphone records once the speed has settled at this step. 2000 ms is the campaign default; longer recordings average more spectra but heat the motor.',
  sample_rate:
    'Samples per second for every microphone. 48 000 Hz covers the whole 20 Hz–20 kHz band and is safe for six USB mics on one hub. Pick 44 100 Hz only if a device refuses 48 kHz.',
  stabilize_window:
    'Number of consecutive stand telemetry samples (about 33 per second) whose RPM readings must all lie within the tolerance before recording starts. 10 samples is about 0.3 s.',
  stabilize_tolerance:
    'Largest RPM spread allowed inside the stabilize window for the speed to count as settled. Smaller is stricter and waits longer.',
  stabilize_timeout:
    'If the speed has not settled within this many seconds the capture stops with an error instead of recording an unsettled step.',
  trigger_sync:
    'Aligns the microphone recordings on the first loud onset (block RMS above the threshold in dBFS), so every channel starts at the same instant. A source already running when the recording starts is left untouched; UMIK-2s cannot be clock-locked in hardware.',
};

export const CUTOFF_HELP = {
  general:
    'Tick a channel and the server forces the ESC signal to 1000 µs the moment its reading crosses the threshold in the chosen direction. A trip stays latched until you reset it on the Tyto stand card. Push the table to the stand before every powered capture; cutoffs reset on every server restart.',
  direction:
    '"Above" trips when the reading rises over the threshold (current, RPM, thrust, torque, temperature). "Below" trips when it falls under it (supply voltage sagging).',
  threshold: 'The value, in the channel unit, at which the cutoff trips.',
  channels: {
    current: 'Motor current measured by the stand. Trip above the motor or ESC rating.',
    voltage: 'Supply voltage at the stand. Trip below to catch a bench supply that is current-limiting (a supply sagging to 8 V spun one propeller off-speed).',
    rpm: 'Shaft speed from the stand’s optical or electrical probe. Trip above the propeller’s rated speed.',
    thrust: 'Net thrust after tare, in newtons. Trip above what the rig mount is rated for.',
    torque: 'Shaft torque after tare, in newton-metres.',
    temp0: 'Temperature probe 0, normally on the motor can.',
    temp1: 'Temperature probe 1 (unused on this rig unless a probe is fitted).',
    temp2: 'Temperature probe 2 (unused on this rig unless a probe is fitted).',
  } as Record<string, string>,
};

export const COMPAT_HELP = {
  general:
    'Two captures at the same ESC signal are shown as one Results point only when every channel agrees within its tolerance. Loosen these if a repeat capture of the same article lands as a separate sidebar entry; tighten them if unrelated captures merge.',
  abs: 'Absolute tolerance in the channel unit. The pair passes when the difference is at most this value, whatever the level.',
  rel: 'Relative tolerance as a fraction of the mean of the two readings (0.05 is 5 %). Whichever of absolute and relative is larger applies.',
};
