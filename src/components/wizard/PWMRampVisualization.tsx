interface Step {
  pwm_us: number;
  recording_ms: number;
}

interface Props {
  steps: Step[];
}

const W = 600;
const H = 200;
const PAD_L = 50;
const PAD_R = 16;
const PAD_T = 24;
const PAD_B = 40;
const innerW = W - PAD_L - PAD_R;
const innerH = H - PAD_T - PAD_B;

const PWM_MIN = 1000;
const PWM_MAX = 2000;
const Y_TICKS = [1000, 1250, 1500, 1750, 2000];

const STROKE = '#818cf8';
const FILL = 'rgba(129, 140, 248, 0.15)';
const GRID = '#374151';
const LABEL = '#9ca3af';
const TEXT = '#e5e7eb';

export function PWMRampVisualization({ steps }: Props) {
  if (steps.length === 0) {
    return (
      <div className="bg-gray-900/40 border border-gray-700 rounded-md p-6 text-center text-sm text-gray-500 italic">
        Add a PWM step to see the ramp visualization.
      </div>
    );
  }

  const totalMs = Math.max(1, steps.reduce((s, st) => s + st.recording_ms, 0));
  const startTimes: number[] = [];
  let acc = 0;
  for (const st of steps) {
    startTimes.push(acc);
    acc += st.recording_ms;
  }

  const xScale = (t: number) => PAD_L + (t / totalMs) * innerW;
  const yScale = (pwm: number) =>
    PAD_T + (1 - (pwm - PWM_MIN) / (PWM_MAX - PWM_MIN)) * innerH;

  // Build the staircase: idle → step1 → step2 → ... → idle
  const pts: { x: number; y: number }[] = [];
  pts.push({ x: xScale(0), y: yScale(PWM_MIN) });
  steps.forEach((st, i) => {
    const t0 = startTimes[i];
    const t1 = t0 + st.recording_ms;
    const y = yScale(st.pwm_us);
    pts.push({ x: xScale(t0), y });
    pts.push({ x: xScale(t1), y });
  });
  pts.push({ x: xScale(totalMs), y: yScale(PWM_MIN) });

  const polylinePoints = pts.map((p) => `${p.x},${p.y}`).join(' ');
  // closed polygon for fill
  const polygonPoints =
    polylinePoints + ` ${xScale(totalMs)},${yScale(PWM_MIN)} ${xScale(0)},${yScale(PWM_MIN)}`;

  return (
    <div className="bg-gray-900/40 border border-gray-700 rounded-md p-2">
      <svg
        viewBox={`0 0 ${W} ${H}`}
        preserveAspectRatio="xMidYMid meet"
        className="w-full h-auto"
        role="img"
        aria-label="PWM ramp visualization"
      >
        {/* horizontal grid */}
        {Y_TICKS.map((pwm) => (
          <g key={pwm}>
            <line
              x1={PAD_L}
              y1={yScale(pwm)}
              x2={W - PAD_R}
              y2={yScale(pwm)}
              stroke={GRID}
              strokeDasharray={pwm === PWM_MIN ? '0' : '2 3'}
              strokeWidth={0.5}
            />
            <text
              x={PAD_L - 6}
              y={yScale(pwm) + 4}
              textAnchor="end"
              fill={LABEL}
              fontSize="11"
              fontFamily="ui-monospace, monospace"
            >
              {pwm}
            </text>
          </g>
        ))}

        {/* axis labels */}
        <text
          x={6}
          y={PAD_T + innerH / 2}
          textAnchor="middle"
          fill={LABEL}
          fontSize="10"
          transform={`rotate(-90 6 ${PAD_T + innerH / 2})`}
        >
          PWM (µs)
        </text>
        <text x={W / 2} y={H - 6} textAnchor="middle" fill={LABEL} fontSize="10">
          time (ms)
        </text>

        {/* filled area + line */}
        <polygon points={polygonPoints} fill={FILL} />
        <polyline points={polylinePoints} fill="none" stroke={STROKE} strokeWidth={2} />

        {/* per-step markers + labels */}
        {steps.map((st, i) => {
          const t0 = startTimes[i];
          const t1 = t0 + st.recording_ms;
          const tMid = (t0 + t1) / 2;
          const y = yScale(st.pwm_us);
          const x0 = xScale(t0);
          const x1 = xScale(t1);
          const xMid = xScale(tMid);
          return (
            <g key={i}>
              {/* step boundary marker */}
              <line
                x1={x0}
                y1={y}
                x2={x0}
                y2={H - PAD_B}
                stroke={GRID}
                strokeDasharray="2 2"
                strokeWidth={0.5}
              />
              {/* PWM value label above the plateau */}
              {x1 - x0 > 30 && (
                <text
                  x={xMid}
                  y={y - 6}
                  textAnchor="middle"
                  fill={TEXT}
                  fontSize="11"
                  fontFamily="ui-monospace, monospace"
                >
                  {st.pwm_us}µs
                </text>
              )}
              {/* recording duration below */}
              {x1 - x0 > 30 && (
                <text
                  x={xMid}
                  y={H - PAD_B + 14}
                  textAnchor="middle"
                  fill={LABEL}
                  fontSize="10"
                  fontFamily="ui-monospace, monospace"
                >
                  {st.recording_ms}ms
                </text>
              )}
              {/* step number */}
              <text
                x={xMid}
                y={H - 6}
                textAnchor="middle"
                fill={LABEL}
                fontSize="9"
              >
                #{i + 1}
              </text>
            </g>
          );
        })}

        {/* total duration */}
        <text
          x={W - PAD_R}
          y={PAD_T - 8}
          textAnchor="end"
          fill={LABEL}
          fontSize="10"
        >
          total recording: {(totalMs / 1000).toFixed(2)}s · {steps.length} step{steps.length === 1 ? '' : 's'}
        </text>
      </svg>
    </div>
  );
}
