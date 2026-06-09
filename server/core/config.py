import tomllib
from pathlib import Path

from pydantic import BaseModel, Field


class TytoCalibrationConfig(BaseModel):
    """Tyto Robotics 1585 calibration constants. Defaults match Paweł's unit."""

    hinge_distance: float = 0.07492
    cal_poles: int = 14
    cal_hinge_left: float = 1.2100092475098374
    cal_hinge_right: float = 1.2590952216896254
    cal_left: float = 0.9663293361785854
    cal_right: float = -0.9575068323376389
    cal_thrust: float = -0.9516456828857573


class TytoConfig(BaseModel):
    enabled: bool = False
    tty: str = "/dev/ttyUSB0"
    poll_period_seconds: float = Field(default=0.03, gt=0.0)
    calibration: TytoCalibrationConfig = TytoCalibrationConfig()


class ServerConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = Field(default=8000, gt=0, le=65535)


class Config(BaseModel):
    tyto: TytoConfig = TytoConfig()
    server: ServerConfig = ServerConfig()


def load_config(path: Path | None = None) -> Config:
    p = path if path is not None else Path("config.toml")
    if not p.exists():
        return Config()
    with p.open("rb") as f:
        return Config.model_validate(tomllib.load(f))
