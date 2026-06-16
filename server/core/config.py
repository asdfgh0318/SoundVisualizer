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


class ResearchTreeConfig(BaseModel):
    """Optional integration with the duct-research-tree editor (separate service,
    typically running alongside this server on the same Pi). When `enabled`, the
    Capture wizard surfaces an active-nodes picker and pushes the SoundVis
    Results URL back into the picked node on a successful capture."""

    enabled: bool = False
    # URL the SoundVis backend uses to reach research-tree's serve.py.
    # On the Pi: http://localhost:8123 (loopback to the local research-tree service).
    base_url: str = "http://localhost:8123"
    # Base URL that the SoundVis Results page is reachable at from the *browser*
    # that opens the research-tree node — i.e. the URL pushed back as
    # `soundVisualizerLink`. Defaults to the request's own origin if empty.
    public_url: str = ""


class Config(BaseModel):
    tyto: TytoConfig = TytoConfig()
    server: ServerConfig = ServerConfig()
    research_tree: ResearchTreeConfig = ResearchTreeConfig()


def load_config(path: Path | None = None) -> Config:
    p = path if path is not None else Path("config.toml")
    if not p.exists():
        return Config()
    with p.open("rb") as f:
        return Config.model_validate(tomllib.load(f))
