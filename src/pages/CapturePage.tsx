import { useEffect, useRef } from 'react';
import { WS_BASE } from '../api/base';
import { api, ApiError } from '../api/client';
import type {
  CaptureMicSpecRun,
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
  const reset = useWizardStore((s) => s.reset);

  const mics = useSetupStore((s) => s.mics);
  const cutoffs = useSetupStore((s) => s.cutoffs);
  const cutoffsConfigured = Object.values(cutoffs).some((c) => c.enabled);

  const isLiveRunning = phase === 'running';
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
    research_tree_node_id: form.research_tree_node_id,
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

  const onAbort = async () => {
    try {
      await api.abortCaptureRun();
    } catch (e) {
      setError((e as ApiError).message);
    }
  };

  const onNew = () => reset();

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Capture</h1>
          <p className="text-sm text-gray-400 mt-1">
            Drive the Tyto stand through an ESC signal ramp, record audio per step, save measurements.
          </p>
        </div>
        {phase !== 'form' && phase !== 'running' && (
          <Button variant="ghost" onClick={() => reset()}>Start over</Button>
        )}
      </header>

      {phase === 'form' && <WizardForm />}

      {phase === 'review' && (
        <ReviewSummary
          form={form}
          mics={mics}
          cutoffsConfigured={cutoffsConfigured}
          onBack={() => setPhase('form')}
          onConfirm={() => setPhase('safety')}
        />
      )}

      {phase === 'safety' && (
        <SafetyModal
          cutoffsConfigured={cutoffsConfigured}
          onCancel={() => setPhase('review')}
          onConfirm={startCapture}
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
