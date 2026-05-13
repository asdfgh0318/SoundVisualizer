"""Smoke tests for the psychoacoustics pipeline. We don't try to hit absolute
sone/acum/asper targets — those depend on dB SPL calibration we don't apply
here. Instead we verify:
  - The pipeline returns finite, non-negative values.
  - Loudness scales monotonically with amplitude.
  - PA scales monotonically with amplitude.
  - Cache on disk avoids recomputation.
"""

from datetime import UTC, datetime, timedelta

import numpy as np
import pytest
from fastapi.testclient import TestClient

from server.api.schemas import AcousticMeasurementMeta, Key, MeasurementHalf
from server.core.psychoacoustics import (
    compute_metrics,
    psychoacoustic_annoyance,
)
from server.core.wav import write_wav_float32
from server.main import app
from server.store import keys as keys_store
from server.store import measurements as meas_store
from server.store import psychoacoustics as psy_store
from server.store.paths import measurement_dir


@pytest.fixture(autouse=True)
def _data_dir(tmp_path, monkeypatch):
    monkeypatch.setenv("SOUNDVIS_DATA", str(tmp_path))
    return tmp_path


@pytest.fixture
def client():
    return TestClient(app)


def _sine(amp: float, freq_hz: float = 1000.0, duration_s: float = 1.5, fs: int = 48000) -> np.ndarray:
    n = int(fs * duration_s)
    t = np.arange(n) / fs
    return (amp * np.sin(2 * np.pi * freq_hz * t)).astype(np.float32)


def test_pa_formula_matches_zwicker_definition():
    # Hand-checked: N=10, S=2.0 (so wS active), R=0.3, F=0
    # wS = (2.0 - 1.75) * 0.25 * log10(10 + 10) = 0.25 * 0.25 * 1.301 = 0.0813
    # wFR = (2.18 / 10^0.4) * (0.4 * 0 + 0.6 * 0.3) = (2.18 / 2.512) * 0.18 = 0.156
    # PA = 10 * (1 + sqrt(0.0813^2 + 0.156^2)) = 10 * (1 + 0.176) = 11.76
    pa = psychoacoustic_annoyance(loudness_sone=10.0, sharpness_acum=2.0,
                                  roughness_asper=0.3, fluctuation_vacil=0.0)
    assert 11.7 < pa < 11.85


def test_pa_below_sharpness_threshold_drops_wS():
    pa_below = psychoacoustic_annoyance(10.0, 1.5, 0.3, 0.0)  # S<1.75 → wS=0
    pa_above = psychoacoustic_annoyance(10.0, 2.0, 0.3, 0.0)  # S>1.75 → wS>0
    assert pa_above > pa_below


def test_pa_zero_loudness_returns_zero():
    assert psychoacoustic_annoyance(0.0, 5.0, 0.5, 0.5) == 0.0


def test_compute_metrics_returns_finite_values():
    audio = _sine(0.1)
    m = compute_metrics(audio, 48000)
    assert m.loudness_sone > 0
    assert m.sharpness_acum > 0
    assert m.roughness_asper >= 0
    assert m.fluctuation_vacil == 0.0
    assert m.fluctuation_assumed_zero is True
    assert m.annoyance > 0
    # All finite
    for v in (m.loudness_sone, m.sharpness_acum, m.roughness_asper, m.annoyance):
        assert np.isfinite(v)


def test_loudness_scales_with_amplitude():
    quiet = compute_metrics(_sine(0.05), 48000)
    loud = compute_metrics(_sine(0.5), 48000)
    assert loud.loudness_sone > quiet.loudness_sone
    assert loud.annoyance > quiet.annoyance


def test_compute_metrics_handles_too_short_audio():
    audio = np.zeros(100, dtype=np.float32)
    m = compute_metrics(audio, 48000)
    assert m.loudness_sone == 0
    assert m.annoyance == 0


def _make_acoustic(slug: str, audio: np.ndarray, fs: int = 48000):
    t = datetime.now(UTC)
    meta = AcousticMeasurementMeta(
        t_start=t,
        t_end=t + timedelta(seconds=1),
        pwm_setpoint=1500,
        mic_serial="X1",
        elevation_deg=0.0,
        half=MeasurementHalf.TOP,
        sample_rate=fs,
    )
    saved = meas_store.create_measurement(slug, meta)
    write_wav_float32(measurement_dir(slug, saved.id) / "audio.wav", audio, fs)
    return saved


def test_endpoint_computes_and_caches(client, tmp_path):
    k = Key(motor="m", propeller="p", shroud="s", notes="n")
    keys_store.create_key(k)
    saved = _make_acoustic(k.slug, _sine(0.1))

    cache = psy_store.cache_path(measurement_dir(k.slug, saved.id))
    assert not cache.exists()

    r = client.get(f"/keys/{k.slug}/measurements/{saved.id}/psychoacoustics")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["loudness_sone"] > 0
    assert body["annoyance"] > 0

    # Cache file exists after first request
    assert cache.exists()

    # Second request returns same values (from cache) — make a unique signature
    r2 = client.get(f"/keys/{k.slug}/measurements/{saved.id}/psychoacoustics")
    assert r2.status_code == 200
    assert r2.json() == body


def test_endpoint_404_on_missing(client):
    k = Key(motor="m", propeller="p", shroud="s", notes="n")
    keys_store.create_key(k)
    r = client.get(f"/keys/{k.slug}/measurements/nope/psychoacoustics")
    assert r.status_code == 404
