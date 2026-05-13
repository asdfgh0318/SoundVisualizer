"""On-disk cache for computed psychoacoustic metrics — written next to audio.wav."""

from pathlib import Path

from server.core.psychoacoustics import PsychoacousticMetrics


def cache_path(measurement_dir_path: Path) -> Path:
    return measurement_dir_path / "psychoacoustics.json"


def load(measurement_dir_path: Path) -> PsychoacousticMetrics | None:
    p = cache_path(measurement_dir_path)
    if not p.exists():
        return None
    return PsychoacousticMetrics.model_validate_json(p.read_text())


def save(measurement_dir_path: Path, metrics: PsychoacousticMetrics) -> None:
    p = cache_path(measurement_dir_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(metrics.model_dump_json(indent=2))
