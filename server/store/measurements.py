from datetime import UTC

from pydantic import TypeAdapter

from server.api.schemas import (
    AcousticMeasurementMeta,
    MeasurementMeta,
)
from server.store.paths import measurement_dir, measurements_dir

_adapter: TypeAdapter[MeasurementMeta] = TypeAdapter(MeasurementMeta)


def make_measurement_id(meta: MeasurementMeta) -> str:
    ts = meta.t_start.astimezone(UTC).strftime("%Y-%m-%dT%H-%M-%S-%f")
    parts = [ts, meta.type]
    if isinstance(meta, AcousticMeasurementMeta):
        parts.extend([meta.half.value, f"mic-{meta.mic_serial}"])
    return "__".join(parts)


def list_measurements(key_slug: str) -> list[MeasurementMeta]:
    d = measurements_dir(key_slug)
    if not d.exists():
        return []
    out: list[MeasurementMeta] = []
    for sub in sorted(d.iterdir()):
        mf = sub / "meta.json"
        if not mf.exists():
            continue
        out.append(_adapter.validate_json(mf.read_text()))
    return out


def get_measurement(key_slug: str, meas_id: str) -> MeasurementMeta | None:
    mf = measurement_dir(key_slug, meas_id) / "meta.json"
    if not mf.exists():
        return None
    return _adapter.validate_json(mf.read_text())


def create_measurement(
    key_slug: str,
    meta: MeasurementMeta,
    *,
    audio_bytes: bytes | None = None,
    telemetry_csv: bytes | None = None,
    norsonic_txt: bytes | None = None,
) -> MeasurementMeta:
    if not meta.id:
        meta = meta.model_copy(update={"id": make_measurement_id(meta)})

    d = measurement_dir(key_slug, meta.id)
    d.mkdir(parents=True, exist_ok=True)
    (d / "meta.json").write_bytes(_adapter.dump_json(meta, indent=2))
    if audio_bytes is not None:
        (d / "audio.wav").write_bytes(audio_bytes)
    if telemetry_csv is not None:
        (d / "telemetry.csv").write_bytes(telemetry_csv)
    if norsonic_txt is not None:
        (d / "norsonic.txt").write_bytes(norsonic_txt)
    return meta
