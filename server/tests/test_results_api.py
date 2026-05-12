from datetime import UTC, datetime, timedelta

import numpy as np
import pytest
from fastapi.testclient import TestClient

from server.api.schemas import (
    AcousticMeasurementMeta,
    Key,
    MeasurementHalf,
    PerformanceMeasurementMeta,
)
from server.core.wav import write_wav_float32
from server.main import app
from server.store import keys, measurements
from server.store.paths import measurement_dir


@pytest.fixture(autouse=True)
def _data_dir(tmp_path, monkeypatch):
    monkeypatch.setenv("SOUNDVIS_DATA", str(tmp_path))
    return tmp_path


@pytest.fixture
def client():
    return TestClient(app)


def _make_key():
    k = Key(motor="m", propeller="p", shroud="s", notes="n")
    keys.create_key(k)
    return k


def _write_acoustic(slug: str, t_start, mic: str, elev: float, half: MeasurementHalf, pwm: int):
    sr = 48000
    t = np.arange(8192) / sr
    audio = (0.5 * np.sin(2 * np.pi * 1000 * t)).astype(np.float32)
    meta = AcousticMeasurementMeta(
        t_start=t_start,
        t_end=t_start + timedelta(seconds=1),
        pwm_setpoint=pwm,
        mic_serial=mic,
        elevation_deg=elev,
        half=half,
        sample_rate=sr,
    )
    saved = measurements.create_measurement(slug, meta)
    write_wav_float32(measurement_dir(slug, saved.id) / "audio.wav", audio, sr)
    return saved


def _write_performance(slug: str, t_start, pwm: int):
    meta = PerformanceMeasurementMeta(
        t_start=t_start,
        t_end=t_start + timedelta(seconds=1),
        pwm_setpoint=pwm,
    )
    csv = (
        b"t_offset_s,thrust_n,torque_nm,current_a,voltage_v,rpm,"
        b"temp0_c,temp1_c,temp2_c,vibration\n"
        b"0.000,5.10,0.51,4.00,16.10,12000,35.0,32.0,30.0,40\n"
        b"0.030,5.20,0.52,4.10,16.05,12010,35.5,32.2,30.1,42\n"
    )
    saved = measurements.create_measurement(slug, meta, telemetry_csv=csv)
    return saved


def test_pwm_points_groups_by_t_start(client):
    k = _make_key()
    t1 = datetime.now(UTC)
    t2 = t1 + timedelta(seconds=10)
    _write_performance(k.slug, t1, 1200)
    _write_acoustic(k.slug, t1, "8100001", 0.0, MeasurementHalf.TOP, 1200)
    _write_acoustic(k.slug, t1, "8100002", 45.0, MeasurementHalf.TOP, 1200)
    _write_performance(k.slug, t2, 1500)
    _write_acoustic(k.slug, t2, "8100001", 0.0, MeasurementHalf.TOP, 1500)

    r = client.get(f"/keys/{k.slug}/pwm_points")
    assert r.status_code == 200
    points = r.json()
    assert len(points) == 2
    p1, p2 = points
    assert p1["pwm_us"] == 1200
    assert p1["half"] == "top"
    assert len(p1["acoustic"]) == 2
    # acoustic sorted by elevation desc
    assert p1["acoustic"][0]["elevation_deg"] == 45.0
    assert p1["acoustic"][1]["elevation_deg"] == 0.0
    assert p2["pwm_us"] == 1500


def test_fft_returns_peak_at_1khz(client):
    k = _make_key()
    saved = _write_acoustic(k.slug, datetime.now(UTC), "X", 0.0, MeasurementHalf.TOP, 1500)
    r = client.get(f"/keys/{k.slug}/measurements/{saved.id}/fft")
    assert r.status_code == 200, r.text
    body = r.json()
    freqs = body["frequencies"]
    mags = body["magnitudes_db"]
    peak_idx = max(range(len(mags)), key=lambda i: mags[i])
    assert abs(freqs[peak_idx] - 1000.0) < 30
    assert body["calibrated"] is False


def test_fft_404_on_missing_measurement(client):
    k = _make_key()
    r = client.get(f"/keys/{k.slug}/measurements/nope/fft")
    assert r.status_code == 404


def test_fft_400_on_performance_measurement(client):
    k = _make_key()
    saved = _write_performance(k.slug, datetime.now(UTC), 1200)
    r = client.get(f"/keys/{k.slug}/measurements/{saved.id}/fft")
    assert r.status_code == 400


def test_performance_summary(client):
    k = _make_key()
    saved = _write_performance(k.slug, datetime.now(UTC), 1500)
    r = client.get(f"/keys/{k.slug}/measurements/{saved.id}/performance_summary")
    assert r.status_code == 200
    body = r.json()
    assert body["n_samples"] == 2
    assert abs(body["thrust_n_mean"] - 5.15) < 0.001
    assert body["thrust_n_max"] == 5.20
    assert abs(body["voltage_v_mean"] - 16.075) < 0.001


def test_performance_summary_404_on_acoustic(client):
    k = _make_key()
    saved = _write_acoustic(k.slug, datetime.now(UTC), "X", 0.0, MeasurementHalf.TOP, 1500)
    r = client.get(f"/keys/{k.slug}/measurements/{saved.id}/performance_summary")
    assert r.status_code == 404
