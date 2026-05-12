from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from server.api.schemas import (
    AcousticMeasurementMeta,
    Key,
    MeasurementHalf,
    PerformanceMeasurementMeta,
)
from server.main import app
from server.store import keys, measurements


@pytest.fixture(autouse=True)
def _data_dir(tmp_path, monkeypatch):
    monkeypatch.setenv("SOUNDVIS_DATA", str(tmp_path))
    return tmp_path


@pytest.fixture
def client():
    return TestClient(app)


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_slug_is_stable():
    k = Key(motor="T-Motor F60", propeller="HQ 5x4.3", shroud="none", notes="seed")
    assert k.slug == "t-motor-f60__hq-5x4-3__none__seed"


def test_create_and_read_key_via_store():
    k = Key(motor="m1", propeller="p1", shroud="s1", notes="n1")
    keys.create_key(k)
    fetched = keys.get_key(k.slug)
    assert fetched is not None
    assert fetched.motor == "m1"
    assert [x.slug for x in keys.list_keys()] == [k.slug]


def test_create_measurement_roundtrip():
    k = Key(motor="m", propeller="p", shroud="s", notes="n")
    keys.create_key(k)
    t = datetime.now(UTC).replace(microsecond=0)
    meta = AcousticMeasurementMeta(
        t_start=t,
        t_end=t + timedelta(seconds=1),
        pwm_setpoint=1500,
        mic_serial="8100001",
        elevation_deg=45.0,
        half=MeasurementHalf.TOP,
    )
    saved = measurements.create_measurement(k.slug, meta, audio_bytes=b"\x00" * 8)
    assert saved.id != ""
    assert "mic-8100001" in saved.id
    assert "top" in saved.id

    listed = measurements.list_measurements(k.slug)
    assert len(listed) == 1
    assert listed[0].id == saved.id


def test_performance_measurement_id_format():
    k = Key(motor="m", propeller="p", shroud="s", notes="n")
    keys.create_key(k)
    t = datetime.now(UTC).replace(microsecond=0)
    meta = PerformanceMeasurementMeta(
        t_start=t, t_end=t + timedelta(seconds=5), pwm_setpoint=1500
    )
    saved = measurements.create_measurement(k.slug, meta, telemetry_csv=b"t\n0.0\n")
    assert saved.id.endswith("__performance")


def test_api_create_key_and_post_measurement(client):
    payload = {"motor": "T-Motor F60", "propeller": "HQ 5x4", "shroud": "none", "notes": "smoke"}
    r = client.post("/keys", json=payload)
    assert r.status_code == 201, r.text
    slug = r.json()["slug"]

    t = datetime.now(UTC).replace(microsecond=0).isoformat()
    meta = {
        "type": "acoustic",
        "t_start": t,
        "t_end": t,
        "pwm_setpoint": 1500,
        "mic_serial": "8100001",
        "elevation_deg": 45.0,
        "half": "top",
    }
    r = client.post(f"/keys/{slug}/measurements", json=meta)
    assert r.status_code == 201, r.text
    assert r.json()["id"] != ""

    r = client.get(f"/keys/{slug}/measurements")
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_api_404_on_unknown_key(client):
    r = client.get("/keys/does__not__exist__here")
    assert r.status_code == 404


def test_api_dev_seed(client):
    r = client.post("/dev/seed")
    assert r.status_code == 200, r.text
    body = r.json()
    # 2 halves * 2 PWM steps * (1 performance + 4 acoustic) = 4 perf + 16 acoustic
    assert len(body["performance"]) == 4
    assert len(body["acoustic"]) == 16
