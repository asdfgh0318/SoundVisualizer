from datetime import datetime
from enum import StrEnum
from typing import Annotated, Literal

from pydantic import BaseModel, Field, computed_field

from server.store.paths import key_slug


class Key(BaseModel):
    motor: str
    propeller: str
    shroud: str
    notes: str

    @computed_field  # type: ignore[prop-decorator]
    @property
    def slug(self) -> str:
        return key_slug(self.motor, self.propeller, self.shroud, self.notes)


class MeasurementHalf(StrEnum):
    TOP = "top"
    BOTTOM = "bottom"


class _BaseMeasurementMeta(BaseModel):
    id: str = ""
    t_start: datetime
    t_end: datetime
    pwm_setpoint: int | None = None


class AcousticMeasurementMeta(_BaseMeasurementMeta):
    type: Literal["acoustic"] = "acoustic"
    mic_serial: str
    elevation_deg: float
    azimuth_deg: float | None = None
    half: MeasurementHalf
    sample_rate: int = 48000
    calibration_file_id: str | None = None


class PerformanceMeasurementMeta(_BaseMeasurementMeta):
    type: Literal["performance"] = "performance"


class NorsonicMeasurementMeta(_BaseMeasurementMeta):
    type: Literal["norsonic"] = "norsonic"


MeasurementMeta = Annotated[
    AcousticMeasurementMeta | PerformanceMeasurementMeta | NorsonicMeasurementMeta,
    Field(discriminator="type"),
]


class CutoffChannel(BaseModel):
    enabled: bool = False
    threshold: float = 0.0
    # "above" trips when measured value > threshold (overcurrent, overheat, overrev).
    # "below" trips when measured value < threshold (undervoltage / battery sag).
    direction: Literal["above", "below"] = "above"


class CutoffTriggers(BaseModel):
    current: CutoffChannel = CutoffChannel()
    voltage: CutoffChannel = CutoffChannel(direction="below")
    rpm: CutoffChannel = CutoffChannel()
    thrust: CutoffChannel = CutoffChannel()
    torque: CutoffChannel = CutoffChannel()
    temp0: CutoffChannel = CutoffChannel()
    temp1: CutoffChannel = CutoffChannel()
    temp2: CutoffChannel = CutoffChannel()


class MicPlacement(BaseModel):
    serial: str
    usb_path: str | None = None
    top_elevation_deg: float | None = None
    bottom_elevation_deg: float | None = None
    calibration_file_id: str | None = None


class FFTConfig(BaseModel):
    window: Literal["hann"] = "hann"
    size: int = 4096
    overlap: float = 0.5


class SetupConfig(BaseModel):
    mics: list[MicPlacement] = []
    cutoffs: CutoffTriggers = CutoffTriggers()
    fft: FFTConfig = FFTConfig()
    sample_rate: int = 48000


class PWMStep(BaseModel):
    pwm_us: int = Field(ge=1000, le=2000)
    recording_ms: int = Field(ge=100, le=60_000)


class KeyFields(BaseModel):
    motor: str
    propeller: str
    shroud: str
    notes: str


class CaptureRunPhase(StrEnum):
    IDLE = "idle"
    STARTING = "starting"
    SETTING_PWM = "setting_pwm"
    STABILIZING = "stabilizing"
    RECORDING = "recording"
    WRITING = "writing"
    SPOOLING_DOWN = "spooling_down"
    COMPLETED = "completed"
    FAILED = "failed"
    ABORTED = "aborted"


class CaptureRunStatus(BaseModel):
    run_id: str
    state: Literal["idle", "running", "completed", "failed", "aborted"] = "idle"
    phase: CaptureRunPhase = CaptureRunPhase.IDLE
    half: MeasurementHalf | None = None
    key_slug: str | None = None
    current_step: int = 0
    total_steps: int = 0
    current_pwm_us: int | None = None
    measurement_ids: list[str] = []
    error: str | None = None


class MicPresetEntry(BaseModel):
    """Portable mic config — no USB device index since that shifts per machine/boot."""

    serial: str
    top_elevation_deg: float | None = None
    bottom_elevation_deg: float | None = None
    calibration_file_id: str | None = None


class SetupPreset(BaseModel):
    id: str
    name: str
    created_at: datetime
    mics: list[MicPresetEntry]
