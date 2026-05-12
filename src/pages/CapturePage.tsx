import { useEffect, useRef, useState } from 'react';
import { WS_BASE } from '../api/base';
import { api, ApiError } from '../api/client';
import type {
  CaptureHalfRunRequest,
  CaptureMicSpecRun,
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
  const reset = useWizardStore((s) => s.reset);

  const mics = useSetupStore((s) => s.mics);
  const cutoffs = useSetupStore((s) => s.cutoffs);
  const cutoffsConfigured = Object.values(cutoffs).some((c) => c.enabled);

  const [fakeRunning, setFakeRunning] = useState(false);

  const isRunning = phase === 'running_top' || phase === 'running_bottom';
  const wsUrl = isRunning ? `${WS_BASE}/capture/run/ws` : null;
  const { message: wsStatus } = useWebSocketJson<CaptureRunStatus>(wsUrl, isRunning);
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
    // completed
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
    return {
      key: keyFields(),
      half,
      pwm_steps: form.pwm_steps,
      mics: usableMics,
      ...commonBodyFields(),
    };
  };

  /** For fake captures: use whatever the user configured, filling in synthetic
   * serial/device for missing fields. If no mics configured at all, generate
   * a default 4-elevation set so the polar plot has data to render. */
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
    return {
      key: keyFields(),
      half,
      pwm_steps: form.pwm_steps,
      mics: fakeMics,
      ...commonBodyFields(),
    };
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

  const onSafetyConfirm = () => {
    if (form.run_top) startHalf('top');
    else if (form.run_bottom) startHalf('bottom');
    else {
      setError('No half selected.');
      setPhase('failed');
    }
  };

  const onAbort = async () => {
    try {
      await api.abortCaptureRun();
    } catch (e) {
      setError((e as ApiError).message);
    }
  };

  const onReconfigureConfirm = () => startHalf('bottom');

  const onFakeRun = async () => {
    setError(null);
    setFakeRunning(true);
    const allTopIds: string[] = [];
    const allBottomIds: string[] = [];
    try {
      if (form.run_top) {
        const r = await api.runFakeCapture(buildFakeBody('top'));
        allTopIds.push(...r.measurement_ids);
      }
      if (form.run_bottom) {
        const r = await api.runFakeCapture(buildFakeBody('bottom'));
        allBottomIds.push(...r.measurement_ids);
      }
      setTopIds(allTopIds);
      setBottomIds(allBottomIds);
      const slug = `${form.motor}__${form.propeller}__${form.shroud}__${form.notes}`
        .toLowerCase()
        .replace(/[^a-z0-9_]+/g, '-')
        .replace(/-+/g, '-');
      setStatus({
        run_id: 'fake',
        state: 'completed',
        phase: 'completed',
        half: form.run_bottom ? 'bottom' : 'top',
        key_slug: slug,
        current_step: form.pwm_steps.length,
        total_steps: form.pwm_steps.length,
        current_pwm_us: null,
        measurement_ids: [...allTopIds, ...allBottomIds],
        error: null,
      });
      setPhase('done');
    } catch (e) {
      setError((e as ApiError).message);
      setPhase('failed');
    } finally {
      setFakeRunning(false);
    }
  };

  const onSkipBottom = () => {
    setPhase('done');
  };

  const onNew = () => reset();

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Capture</h1>
          <p className="text-sm text-gray-400 mt-1">
            Drive the Tyto stand through a PWM ramp, record audio per step, save measurements.
          </p>
        </div>
        {phase !== 'form' && phase !== 'running_top' && phase !== 'running_bottom' && (
          <Button variant="ghost" onClick={() => reset()}>
            Start over
          </Button>
        )}
      </header>

      {phase === 'form' && <WizardForm fakeRunning={fakeRunning} onFakeRun={onFakeRun} />}

      {phase === 'review' && (
        <ReviewSummary
          form={form}
          mics={mics}
          cutoffsConfigured={cutoffsConfigured}
          fakeRunning={fakeRunning}
          onBack={() => setPhase('form')}
          onConfirm={() => setPhase('safety')}
          onFakeRun={onFakeRun}
        />
      )}

      {phase === 'safety' && (
        <SafetyModal
          half={form.run_top ? 'top' : 'bottom'}
          cutoffsConfigured={cutoffsConfigured}
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
