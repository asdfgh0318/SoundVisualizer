import { useEffect, useRef } from 'react';
import { WS_BASE } from '../api/base';
import { api, ApiError } from '../api/client';
import type {
  CaptureMicSpecRun,
  CaptureRunPhase,
  CaptureRunRequest,
  CaptureRunStatus,
} from '../api/types';
import { DoneSummary } from '../components/wizard/DoneSummary';
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
  const measurementIds = useWizardStore((s) => s.measurementIds);
  const setMeasurementIds = useWizardStore((s) => s.setMeasurementIds);
  const errorMessage = useWizardStore((s) => s.errorMessage);
  const setError = useWizardStore((s) => s.setError);
  const fakeMode = useWizardStore((s) => s.fakeMode);
  const setFakeMode = useWizardStore((s) => s.setFakeMode);
  const reset = useWizardStore((s) => s.reset);

  const mics = useSetupStore((s) => s.mics);
  const cutoffs = useSetupStore((s) => s.cutoffs);
  const cutoffsConfigured = Object.values(cutoffs).some((c) => c.enabled);

  // WS only used for real captures — fake mode drives status manually.
  const isLiveRunning = phase === 'running' && !fakeMode;
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
    setMeasurementIds(wsStatus.measurement_ids);
    setPhase('done');
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

  const buildBody = (): CaptureRunRequest => {
    const usableMics: CaptureMicSpecRun[] = mics
      .filter((m) => m.serial && m.deviceIndex !== null && form.selected_mic_ids.includes(m.id))
      .map((m) => ({
        serial: m.serial,
        device_index: m.deviceIndex as number,
        elevation_deg: m.elevationDeg ?? 0,
        calibration_file_id: m.calibrationFileId,
      }));
    return {
      key: keyFields(),
      half: 'full',
      pwm_steps: form.pwm_steps,
      mics: usableMics,
      ...commonBodyFields(),
    };
  };

  const buildFakeBody = (): CaptureRunRequest => {
    const selected = form.selected_mic_ids.length > 0
      ? mics.filter((m) => form.selected_mic_ids.includes(m.id))
      : mics;
    let fakeMics: CaptureMicSpecRun[] = selected.map((m, i) => ({
      serial: m.serial || `fake-mic-${i + 1}`,
      device_index: m.deviceIndex ?? 0,
      elevation_deg: m.elevationDeg ?? 0,
      calibration_file_id: m.calibrationFileId,
    }));
    if (fakeMics.length === 0) {
      // Default to a symmetric 9-mic arc covering the whole hemisphere.
      const defaults = [-90, -60, -30, -15, 0, 15, 30, 60, 90];
      fakeMics = defaults.map((e, i) => ({
        serial: `fake-mic-${i + 1}`,
        device_index: 0,
        elevation_deg: e,
        calibration_file_id: null,
      }));
    }
    return {
      key: keyFields(),
      half: 'full',
      pwm_steps: form.pwm_steps,
      mics: fakeMics,
      ...commonBodyFields(),
    };
  };

  const startCapture = async () => {
    setError(null);
    try {
      const r = await api.startCaptureRun(buildBody());
      setActiveRunId(r.run_id);
      lastHandledRunIdRef.current = null;
      setPhase('running');
    } catch (e) {
      setError((e as ApiError).message);
      setPhase('failed');
    }
  };

  const startFakeCapture = async () => {
    setError(null);
    setActiveRunId('fake');
    setPhase('running');

    const body = buildFakeBody();
    const totalSteps = body.pwm_steps.length;

    // Kick off the data write in parallel with the simulated progress UI.
    const dataPromise = api.runFakeCapture(body);

    try {
      for (let i = 0; i < totalSteps; i++) {
        for (const { phase: ph, ms } of FAKE_PHASE_TIMINGS) {
          setStatus({
            run_id: 'fake', state: 'running', phase: ph, half: 'full',
            key_slug: null,
            current_step: i + 1, total_steps: totalSteps,
            current_pwm_us: body.pwm_steps[i].pwm_us,
            measurement_ids: [], error: null,
          });
          await wait(ms);
        }
      }
      setStatus({
        run_id: 'fake', state: 'running', phase: 'spooling_down', half: 'full',
        key_slug: null,
        current_step: totalSteps, total_steps: totalSteps,
        current_pwm_us: null,
        measurement_ids: [], error: null,
      });
      await wait(300);

      const r = await dataPromise;
      setMeasurementIds(r.measurement_ids);

      setStatus({
        run_id: 'fake', state: 'completed', phase: 'completed', half: 'full',
        key_slug: r.key,
        current_step: totalSteps, total_steps: totalSteps,
        current_pwm_us: null,
        measurement_ids: r.measurement_ids, error: null,
      });
      setPhase('done');
    } catch (e) {
      setError((e as ApiError).message);
      setPhase('failed');
    }
  };

  const onSafetyConfirm = () => {
    if (fakeMode) startFakeCapture();
    else startCapture();
  };

  const onAbort = async () => {
    if (fakeMode) {
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

  const onFakeRun = () => {
    setError(null);
    setFakeMode(true);
    setPhase('safety');
  };

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
        {phase !== 'form' && phase !== 'running' && (
          <Button variant="ghost" onClick={() => reset()}>Start over</Button>
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
          cutoffsConfigured={cutoffsConfigured}
          fakeMode={fakeMode}
          onCancel={() => setPhase('review')}
          onConfirm={onSafetyConfirm}
        />
      )}

      {phase === 'running' && <RunningView status={status} onAbort={onAbort} />}

      {phase === 'done' && (
        <DoneSummary
          keySlug={status?.key_slug ?? null}
          measurementIds={measurementIds}
          onNew={onNew}
        />
      )}

      {phase === 'failed' && (
        <Card title="Capture failed">
          <div className="text-red-300 mb-4">{errorMessage ?? 'Unknown error.'}</div>
          <div className="flex items-center gap-3">
            <Button onClick={() => setPhase('form')}>Back to form</Button>
            <Button variant="ghost" onClick={onNew}>Reset everything</Button>
          </div>
        </Card>
      )}
    </div>
  );
}
