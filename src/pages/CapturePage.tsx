import { useEffect, useRef } from 'react';
import { WS_BASE } from '../api/base';
import { api, ApiError } from '../api/client';
import type {
  CaptureHalfRunRequest,
  CaptureMicSpecRun,
  CaptureRunPhase,
  CaptureRunStatus,
  MeasurementHalf,
} from '../api/types';
import { DoneSummary } from '../components/wizard/DoneSummary';
import { ReconfigureModal } from '../components/wizard/ReconfigureModal';
import { ReviewSummary } from '../components/wizard/ReviewSummary';
import { RunningView } from '../components/wizard/RunningView';
import { SafetyModal } from '../components/wizard/SafetyModal';
import { WizardForm } from '../components/wizard/WizardForm';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { useWebSocketJson } from '../hooks/useWebSocketJson';
import { useSetupStore } from '../stores/setupStore';
import { useWizardStore } from '../stores/wizardStore';

const FAKE_PHASE_TIMINGS: { phase: CaptureRunPhase; ms: number }[] = [
  { phase: 'setting_pwm', ms: 150 },
  { phase: 'stabilizing', ms: 350 },
  { phase: 'recording', ms: 500 },
  { phase: 'writing', ms: 200 },
];

const wait = (ms: number) => new Promise<void>((r) => setTimeout(r, ms));

export function CapturePage() {
  const phase = useWizardStore((s) => s.phase);
  const form = useWizardStore((s) => s.form);
  const setPhase = useWizardStore((s) => s.setPhase);
  const setStatus = useWizardStore((s) => s.setStatus);
  const status = useWizardStore((s) => s.status);
  const activeRunId = useWizardStore((s) => s.activeRunId);
  const setActiveRunId = useWizardStore((s) => s.setActiveRunId);
  const topIds = useWizardStore((s) => s.topMeasurementIds);
  const bottomIds = useWizardStore((s) => s.bottomMeasurementIds);
  const setTopIds = useWizardStore((s) => s.setTopIds);
  const setBottomIds = useWizardStore((s) => s.setBottomIds);
  const errorMessage = useWizardStore((s) => s.errorMessage);
  const setError = useWizardStore((s) => s.setError);
  const fakeMode = useWizardStore((s) => s.fakeMode);
  const setFakeMode = useWizardStore((s) => s.setFakeMode);
  const reset = useWizardStore((s) => s.reset);

  const mics = useSetupStore((s) => s.mics);
  const cutoffs = useSetupStore((s) => s.cutoffs);
  const cutoffsConfigured = Object.values(cutoffs).some((c) => c.enabled);

  // WS only used for real captures — fake mode drives status manually.
  const isLiveRunning = (phase === 'running_top' || phase === 'running_bottom') && !fakeMode;
  const wsUrl = isLiveRunning ? `${WS_BASE}/capture/run/ws` : null;
  const { message: wsStatus } = useWebSocketJson<CaptureRunStatus>(wsUrl, isLiveRunning);
  const lastHandledRunIdRef = useRef<string | null>(null);

  useEffect(() => {
    if (!wsStatus) return;
    setStatus(wsStatus);
    if (!activeRunId || wsStatus.run_id !== activeRunId) return;
    if (wsStatus.state !== 'completed' &&
        wsStatus.state !== 'failed' &&
        wsStatus.state !== 'aborted') return;
    if (lastHandledRunIdRef.current === wsStatus.run_id) return;
    lastHandledRunIdRef.current = wsStatus.run_id;

    if (wsStatus.state === 'failed') {
      setError(wsStatus.error ?? 'unknown error');
      setPhase('failed');
      return;
    }
    if (wsStatus.state === 'aborted') {
      setError('Capture aborted.');
      setPhase('failed');
      return;
    }
    if (phase === 'running_top') {
      setTopIds(wsStatus.measurement_ids);
      if (form.run_bottom) setPhase('reconfigure');
      else setPhase('done');
    } else if (phase === 'running_bottom') {
      setBottomIds(wsStatus.measurement_ids);
      setPhase('done');
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [wsStatus]);

  const keyFields = () => ({
    motor: form.motor.trim(),
    propeller: form.propeller.trim(),
    shroud: form.shroud.trim(),
    notes: form.notes.trim(),
  });

  const commonBodyFields = () => ({
    sample_rate: form.sample_rate,
    stabilize_window: form.stabilize_window,
    stabilize_tolerance: form.stabilize_tolerance,
    stabilize_timeout_seconds: form.stabilize_timeout_seconds,
    trigger: form.trigger,
  });

  const buildBody = (half: MeasurementHalf): CaptureHalfRunRequest => {
    const usableMics: CaptureMicSpecRun[] = mics
      .filter(
        (m) => m.serial && m.deviceIndex !== null && form.selected_mic_ids.includes(m.id),
      )
      .map((m) => ({
        serial: m.serial,
        device_index: m.deviceIndex as number,
        elevation_deg:
          (half === 'top' ? m.topElevationDeg : m.bottomElevationDeg) ?? 0,
        calibration_file_id: m.calibrationFileId,
      }));
    return { key: keyFields(), half, pwm_steps: form.pwm_steps, mics: usableMics, ...commonBodyFields() };
  };

  const buildFakeBody = (half: MeasurementHalf): CaptureHalfRunRequest => {
    const selected = form.selected_mic_ids.length > 0
      ? mics.filter((m) => form.selected_mic_ids.includes(m.id))
      : mics;
    let fakeMics: CaptureMicSpecRun[] = selected.map((m, i) => ({
      serial: m.serial || `fake-mic-${i + 1}`,
      device_index: m.deviceIndex ?? 0,
      elevation_deg: (half === 'top' ? m.topElevationDeg : m.bottomElevationDeg) ?? 0,
      calibration_file_id: m.calibrationFileId,
    }));
    if (fakeMics.length === 0) {
      const defaults = half === 'top' ? [0, 30, 60, 90] : [0, -30, -60, -90];
      fakeMics = defaults.map((e, i) => ({
        serial: `fake-mic-${i + 1}`,
        device_index: 0,
        elevation_deg: e,
        calibration_file_id: null,
      }));
    }
    return { key: keyFields(), half, pwm_steps: form.pwm_steps, mics: fakeMics, ...commonBodyFields() };
  };

  const startHalf = async (half: 'top' | 'bottom') => {
    setError(null);
    try {
      const r = await api.startCaptureRun(buildBody(half));
      setActiveRunId(r.run_id);
      lastHandledRunIdRef.current = null;
      setPhase(half === 'top' ? 'running_top' : 'running_bottom');
    } catch (e) {
      setError((e as ApiError).message);
      setPhase('failed');
    }
  };

  /** Fake-mode half: writes synthetic data + plays a simulated progress animation
   *  through the same RunningView the real flow uses. */
  const startFakeHalf = async (half: 'top' | 'bottom') => {
    setError(null);
    setActiveRunId('fake');
    setPhase(half === 'top' ? 'running_top' : 'running_bottom');

    const body = buildFakeBody(half);
    const totalSteps = body.pwm_steps.length;

    // Kick off the data write in parallel with the simulated progress UI.
    const dataPromise = api.runFakeCapture(body);

    try {
      // Animate through each step's lifecycle.
      for (let i = 0; i < totalSteps; i++) {
        for (const { phase: ph, ms } of FAKE_PHASE_TIMINGS) {
          setStatus({
            run_id: 'fake', state: 'running', phase: ph, half,
            key_slug: null,
            current_step: i + 1, total_steps: totalSteps,
            current_pwm_us: body.pwm_steps[i].pwm_us,
            measurement_ids: [], error: null,
          });
          await wait(ms);
        }
      }
      setStatus({
        run_id: 'fake', state: 'running', phase: 'spooling_down', half,
        key_slug: null,
        current_step: totalSteps, total_steps: totalSteps,
        current_pwm_us: null,
        measurement_ids: [], error: null,
      });
      await wait(300);

      // Data was written while we were animating — collect IDs.
      const r = await dataPromise;
      if (half === 'top') setTopIds(r.measurement_ids);
      else setBottomIds(r.measurement_ids);

      setStatus({
        run_id: 'fake', state: 'completed', phase: 'completed', half,
        key_slug: r.key,
        current_step: totalSteps, total_steps: totalSteps,
        current_pwm_us: null,
        measurement_ids: r.measurement_ids, error: null,
      });

      if (half === 'top' && form.run_bottom) {
        setPhase('reconfigure');
      } else {
        setPhase('done');
      }
    } catch (e) {
      setError((e as ApiError).message);
      setPhase('failed');
    }
  };

  const onSafetyConfirm = () => {
    const firstHalf = form.run_top ? 'top' : form.run_bottom ? 'bottom' : null;
    if (!firstHalf) {
      setError('No half selected.');
      setPhase('failed');
      return;
    }
    if (fakeMode) startFakeHalf(firstHalf);
    else startHalf(firstHalf);
  };

  const onAbort = async () => {
    if (fakeMode) {
      // Fake aborts are trivial — just bail to failed state.
      setError('Fake capture aborted.');
      setPhase('failed');
      return;
    }
    try {
      await api.abortCaptureRun();
    } catch (e) {
      setError((e as ApiError).message);
    }
  };

  const onReconfigureConfirm = () => {
    if (fakeMode) startFakeHalf('bottom');
    else startHalf('bottom');
  };

  const onFakeRun = () => {
    setError(null);
    setFakeMode(true);
    setPhase('safety');
  };

  const onSkipBottom = () => setPhase('done');

  const onNew = () => reset();

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Capture</h1>
          <p className="text-sm text-gray-400 mt-1">
            Drive the Tyto stand through a PWM ramp, record audio per step, save measurements.
            {fakeMode && (
              <span className="ml-2 text-amber-400 text-xs uppercase tracking-wide">
                · fake mode (no hardware)
              </span>
            )}
          </p>
        </div>
        {phase !== 'form' && phase !== 'running_top' && phase !== 'running_bottom' && (
          <Button variant="ghost" onClick={() => reset()}>
            Start over
          </Button>
        )}
      </header>

      {phase === 'form' && <WizardForm fakeRunning={false} onFakeRun={onFakeRun} />}

      {phase === 'review' && (
        <ReviewSummary
          form={form}
          mics={mics}
          cutoffsConfigured={cutoffsConfigured}
          fakeRunning={false}
          onBack={() => setPhase('form')}
          onConfirm={() => setPhase('safety')}
          onFakeRun={onFakeRun}
        />
      )}

      {phase === 'safety' && (
        <SafetyModal
          half={form.run_top ? 'top' : 'bottom'}
          cutoffsConfigured={cutoffsConfigured}
          fakeMode={fakeMode}
          onCancel={() => setPhase('review')}
          onConfirm={onSafetyConfirm}
        />
      )}

      {phase === 'running_top' && <RunningView half="top" status={status} onAbort={onAbort} />}
      {phase === 'running_bottom' && (
        <RunningView half="bottom" status={status} onAbort={onAbort} />
      )}

      {phase === 'reconfigure' && (
        <ReconfigureModal
          mics={mics.filter((m) => form.selected_mic_ids.includes(m.id))}
          onCancel={onSkipBottom}
          onConfirm={onReconfigureConfirm}
        />
      )}

      {phase === 'done' && (
        <DoneSummary
          keySlug={status?.key_slug ?? null}
          topIds={topIds}
          bottomIds={bottomIds}
          onNew={onNew}
        />
      )}

      {phase === 'failed' && (
        <Card title="Capture failed">
          <div className="text-red-300 mb-4">{errorMessage ?? 'Unknown error.'}</div>
          <div className="flex items-center gap-3">
            <Button onClick={() => setPhase('form')}>Back to form</Button>
            <Button variant="ghost" onClick={onNew}>
              Reset everything
            </Button>
          </div>
        </Card>
      )}
    </div>
  );
}
