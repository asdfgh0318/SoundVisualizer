"""On-disk cache for computed psychoacoustic metrics — written next to audio.wav."""

from pathlib import Path

from pydantic import BaseModel, ValidationError

from server.core.psychoacoustics import PsychoacousticMetrics

# Bump whenever the computation changes meaning. v2 scales the audio to Pa before
# mosqito; every v1 file (unversioned, arbitrary scale) is wrong by a large
# nonlinear amount, so an unrecognised version is a cache miss, not a fallback.
CACHE_VERSION = 2


class _Envelope(BaseModel):
    version: int
    metrics: PsychoacousticMetrics


def cache_path(measurement_dir_path: Path) -> Path:
    return measurement_dir_path / "psychoacoustics.json"


def load(measurement_dir_path: Path) -> PsychoacousticMetrics | None:
    p = cache_path(measurement_dir_path)
    if not p.exists():
        return None
    try:
        env = _Envelope.model_validate_json(p.read_text())
    except ValidationError:
        return None
    if env.version != CACHE_VERSION:
        return None
    return env.metrics


def save(measurement_dir_path: Path, metrics: PsychoacousticMetrics) -> None:
    p = cache_path(measurement_dir_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(_Envelope(version=CACHE_VERSION, metrics=metrics).model_dump_json(indent=2))
