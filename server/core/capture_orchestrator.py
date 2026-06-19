"""End-to-end capture run for one half (top or bottom).

Before any PWM step runs, tare the stand once: motor is already at idle, so
the load cells just need a moment to settle before re-zeroing. This guards
against false thrust/torque/current readings caused by load-cell drift
between runs. Re-taring between PWM steps would require spooling the motor
down and back up each time — not worth the wear and time.

Per PWM step:
  1. Set Tyto PWM (refuses if watchdog tripped).
  2. Wait for RPM stabilization (with timeout).
  3. Begin Tyto sample window + start audio capture for `step.recording_ms`
     (in a thread, so the asyncio loop keeps polling Tyto).
  4. End Tyto window → write performance measurement (CSV).
  5. Apply trigger sync to mic audios → write per-mic acoustic measurements.
  6. Broadcast status to subscribers after every state change.

After all steps complete, gently ramp PWM back to 1000 µs (10 µs / 100 ms). On
abort or failure, slam PWM to 1000 immediately.

Adapted from Paweł's `measurement_station.meas_series` but writes to our JSON+WAV
filesystem store instead of pickled `OpPointData` objects, captures audio from
UMIK-2s alongside Tyto telemetry, and broadcasts progress over a WebSocket.
"""

import asyncio
import contextlib
import logging
import uuid
from collections.abc import Callable, Sequence
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel

from server.api.schemas import (
    AcousticMeasurementMeta,
    CaptureRunPhase,
    CaptureRunStatus,
    Key,
    KeyFields,
    MeasurementHalf,
    PerformanceMeasurementMeta,
    PWMStep,
)
from server.core.capture import MicCaptureSpec, capture_simultaneous
from server.core.trigger_sync import align_captures
from server.core.wav import write_wav_float32
from server.store import keys as keys_store
from server.store import measurements as meas_store
from server.store.paths import measurement_dir
from server.vendor.pawel.msp import PollResponse
from server.vendor.pawel.thrust_stand import raw_thrust, raw_torque

if TYPE_CHECKING:
    from server.core.thrust_stand_service import TareOffsets, ThrustStandService

log = logging.getLogger(__name__)


class MicSpecRun(BaseModel):
    serial: str
    device_index: int
    elevation_deg: float
    calibration_file_id: str | None = None


class TriggerSyncRun(BaseModel):
    enabled: bool = True
    threshold_db: float = -40.0
    block_size: int = 128
    preroll_samples: int = 480


class CaptureRunRequest(BaseModel):
    """A single capture pass. `half` defaults to FULL (single-pass: mics span
    the whole arc in one shot). Two-pass clients can send half="top"/"bottom"
    to label their measurements explicitly — the orchestrator treats them all
    the same way at the data level."""

    key: KeyFields
    half: MeasurementHalf = MeasurementHalf.FULL
    pwm_steps: list[PWMStep]
    mics: list[MicSpecRun]
    sample_rate: int = 48000
    stabilize_window: int = 10
    stabilize_tolerance: float = 4.0
    stabilize_timeout_seconds: float = 30.0
    trigger: TriggerSyncRun = TriggerSyncRun()
    # Optional duct-research-tree linkage. When set, the orchestrator pushes the
    # SoundVis Results URL back to that node on successful completion.
    research_tree_node_id: str | None = None


def _telemetry_to_csv(
    samples: Sequence[PollResponse], poll_period_s: float, tare: "TareOffsets"
) -> bytes:
    header = (
        "t_offset_s,thrust_n,torque_nm,current_a,voltage_v,rpm,"
        "temp0_c,temp1_c,temp2_c,vibration"
    )
    rows = [header]
    for i, s in enumerate(samples):
        t = i * poll_period_s
        rows.append(
            f"{t:.3f},"
            f"{raw_thrust(s.load_thrust) - tare.thrust_n:.4f},"
            f"{raw_torque(s.load_left, s.load_right) - tare.torque_nm:.4f},"
            f"{s.esc_current - tare.current_a:.4f},"
            f"{s.esc_voltage:.4f},"
            f"{s.rot_e:.1f},"
            f"{s.temp0:.2f},{s.temp1:.2f},{s.temp2:.2f},"
            f"{s.vibration}"
        )
    return ("\n".join(rows) + "\n").encode("utf-8")


class CaptureOrchestrator:
    def __init__(
        self,
        poll_period_seconds: float = 0.03,
        on_completed: Callable[[CaptureRunRequest, CaptureRunStatus], None] | None = None,
        settle_before_tare_s: float = 1.0,
        tare_window_samples: int = 30,
    ):
        self._poll_period_s = poll_period_seconds
        self._settle_before_tare_s = settle_before_tare_s
        self._tare_window_samples = tare_window_samples
        self._status = CaptureRunStatus(run_id="", state="idle")
        self._task: asyncio.Task[None] | None = None
        self._stand_service: ThrustStandService | None = None
        self._subscribers: list[asyncio.Queue[CaptureRunStatus]] = []
        self._current_req: CaptureRunRequest | None = None
        # External hook fired exactly once when a run terminates with state=completed.
        # Used by the research-tree integration to push the SoundVis Results URL back.
        # Synchronous best-effort — callable should never raise.
        self._on_completed = on_completed

    def get_status(self) -> CaptureRunStatus:
        return self._status.model_copy()

    def is_running(self) -> bool:
        return self._task is not None and not self._task.done()

    def subscribe(self) -> asyncio.Queue[CaptureRunStatus]:
        q: asyncio.Queue[CaptureRunStatus] = asyncio.Queue(maxsize=20)
        self._subscribers.append(q)
        return q

    def unsubscribe(self, q: asyncio.Queue[CaptureRunStatus]) -> None:
        if q in self._subscribers:
            self._subscribers.remove(q)

    async def start_run(
        self,
        stand_service: "ThrustStandService",
        req: CaptureRunRequest,
    ) -> CaptureRunStatus:
        if self.is_running():
            raise RuntimeError("a capture run is already in progress")
        if not req.pwm_steps:
            raise ValueError("pwm_steps must not be empty")
        if not req.mics:
            raise ValueError("mics must not be empty")

        self._stand_service = stand_service
        self._current_req = req
        self._status = CaptureRunStatus(
            run_id=uuid.uuid4().hex,
            state="running",
            phase=CaptureRunPhase.STARTING,
            half=req.half,
            total_steps=len(req.pwm_steps),
        )
        await self._broadcast()

        self._task = asyncio.create_task(self._run(req))
        return self.get_status()

    async def abort(self) -> None:
        # Slam PWM first so the motor stops immediately, even before the task notices cancellation.
        if self._stand_service is not None:
            self._stand_service.stand.mot_pwm = 1000
        if self._task and not self._task.done():
            self._task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._task

    async def _run(self, req: CaptureRunRequest) -> None:
        try:
            await self._do_run(req)
            self._status.state = "completed"
            self._status.phase = CaptureRunPhase.COMPLETED
        except asyncio.CancelledError:
            self._status.state = "aborted"
            self._status.phase = CaptureRunPhase.ABORTED
            await self._safe_spool_down_slam()
            await self._broadcast()
            raise
        except Exception as e:
            log.exception("capture run failed")
            self._status.state = "failed"
            self._status.phase = CaptureRunPhase.FAILED
            self._status.error = f"{type(e).__name__}: {e}"
            await self._safe_spool_down_slam()
        await self._broadcast()
        # External completion hook — best-effort, never propagates errors.
        if self._on_completed and self._status.state == "completed":
            try:
                self._on_completed(req, self.get_status())
            except Exception:
                log.exception("on_completed hook raised — swallowing to protect the run")

    async def _do_run(self, req: CaptureRunRequest) -> None:
        assert self._stand_service is not None

        key = Key(**req.key.model_dump())
        if not keys_store.get_key(key.slug):
            keys_store.create_key(key)
        self._status.key_slug = key.slug
        await self._broadcast()

        # One tare before the motor first spins. Re-taring between PWM steps
        # would force a spool-down/spool-up per step — not worth the wear.
        await self._tare_before_spin_up()

        for i, step in enumerate(req.pwm_steps):
            self._status.current_step = i + 1
            self._status.current_pwm_us = step.pwm_us

            self._status.phase = CaptureRunPhase.SETTING_PWM
            await self._broadcast()
            self._stand_service.set_pwm(step.pwm_us)

            self._status.phase = CaptureRunPhase.STABILIZING
            await self._broadcast()
            async with asyncio.timeout(req.stabilize_timeout_seconds):
                await self._stand_service.stand.stabilize_rpm(
                    req.stabilize_window, req.stabilize_tolerance
                )

            await self._capture_step(req, key.slug, step)

        self._status.phase = CaptureRunPhase.SPOOLING_DOWN
        await self._broadcast()
        await self._spool_down_gentle()

    async def _capture_step(
        self,
        req: CaptureRunRequest,
        key_slug: str,
        step: PWMStep,
    ) -> None:
        assert self._stand_service is not None
        stand = self._stand_service.stand

        self._status.phase = CaptureRunPhase.RECORDING
        await self._broadcast()

        pending = stand.start_meas_series()
        t_start = datetime.now(UTC)

        specs = [
            MicCaptureSpec(
                serial=m.serial,
                device_index=m.device_index,
                sample_rate=req.sample_rate,
            )
            for m in req.mics
        ]
        duration_s = step.recording_ms / 1000.0
        results = await asyncio.to_thread(capture_simultaneous, specs, duration_s)

        tyto_samples = stand.finish_meas_series(pending)
        t_end = datetime.now(UTC)

        self._status.phase = CaptureRunPhase.WRITING
        await self._broadcast()

        perf_meta = PerformanceMeasurementMeta(
            t_start=t_start, t_end=t_end, pwm_setpoint=step.pwm_us
        )
        # Tyto samples are computed values; we need the raw PollResponse list to build the CSV.
        # finish_meas_series returns calibrated ThrustStandMeasurement objects. Use raw window:
        n = len(tyto_samples)
        raw_window: Sequence[PollResponse] = stand.samples_raw[-n:] if n else []
        perf_saved = meas_store.create_measurement(
            key_slug,
            perf_meta,
            telemetry_csv=_telemetry_to_csv(
                raw_window, self._poll_period_s, self._stand_service.tare
            ),
        )
        self._status.measurement_ids.append(perf_saved.id)

        audios = [r.audio for r in results]
        if req.trigger.enabled:
            audios = align_captures(
                audios,
                threshold_db=req.trigger.threshold_db,
                block_size=req.trigger.block_size,
                preroll_samples=req.trigger.preroll_samples,
            )

        for mic, audio in zip(req.mics, audios, strict=True):
            meta = AcousticMeasurementMeta(
                t_start=t_start,
                t_end=t_end,
                pwm_setpoint=step.pwm_us,
                mic_serial=mic.serial,
                elevation_deg=mic.elevation_deg,
                half=req.half,
                sample_rate=req.sample_rate,
                calibration_file_id=mic.calibration_file_id,
            )
            saved = meas_store.create_measurement(key_slug, meta)
            write_wav_float32(
                measurement_dir(key_slug, saved.id) / "audio.wav",
                audio,
                req.sample_rate,
            )
            self._status.measurement_ids.append(saved.id)

        await self._broadcast()

    async def _tare_before_spin_up(self) -> None:
        """Re-zero the stand at idle before the motor spins for the first step.

        The motor is at PWM=1000 (idle, no thrust). After a short settling
        window, average the latest at-rest samples and set them as the tare
        baseline so the run's thrust/torque/current readings aren't skewed by
        sensor drift from earlier work.
        """
        assert self._stand_service is not None
        self._status.phase = CaptureRunPhase.TARING
        await self._broadcast()
        # Spool down (no-op if already idle) so the load cells genuinely sit at zero.
        await self._spool_down_gentle()
        await asyncio.sleep(self._settle_before_tare_s)
        self._stand_service.zero(n=self._tare_window_samples)
        await self._broadcast()

    async def _spool_down_gentle(self) -> None:
        if self._stand_service is None:
            return
        stand = self._stand_service.stand
        while stand.mot_pwm > 1000:
            stand.mot_pwm = max(1000, stand.mot_pwm - 10)
            await asyncio.sleep(0.1)

    async def _safe_spool_down_slam(self) -> None:
        try:
            if self._stand_service is not None:
                self._stand_service.stand.mot_pwm = 1000
        except Exception:
            log.exception("failed to slam PWM during cleanup")

    async def _broadcast(self) -> None:
        snap = self._status.model_copy()
        dead: list[asyncio.Queue[Any]] = []
        for q in self._subscribers:
            try:
                if q.full():
                    with contextlib.suppress(asyncio.QueueEmpty):
                        q.get_nowait()
                q.put_nowait(snap)
            except Exception:
                dead.append(q)
        for q in dead:
            self._subscribers.remove(q)
