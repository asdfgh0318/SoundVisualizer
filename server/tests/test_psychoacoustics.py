"""Smoke tests for the psychoacoustics pipeline. We don't try to hit absolute
sone/acum/asper targets — mosqito itself is the thing under test there. Instead
we verify:
  - The pipeline returns finite, non-negative values.
  - Loudness scales monotonically with amplitude (and with the Pa scalar).
  - PA scales monotonically with amplitude.
  - Metrics are flagged absolute only when the audio was scaled to Pa.
  - Cache on disk avoids recomputation, and stale-schema cache files don't.
"""

import json
from datetime import UTC, datetime, timedelta

import numpy as np
import pytest
from fastapi.testclient import TestClient

from server.api.schemas import AcousticMeasurementMeta, Key, MeasurementHalf
from server.core.calibration import parse_umik_calibration
from server.core.psychoacoustics import (
    compute_metrics,
    psychoacoustic_annoyance,
)
from server.core.wav import write_wav_float32
from server.main import app
from server.store import calibration as cal_store
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
    m = compute_metrics(audio, 48000, pa_per_full_scale=None)
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
    quiet = compute_metrics(_sine(0.05), 48000, pa_per_full_scale=None)
    loud = compute_metrics(_sine(0.5), 48000, pa_per_full_scale=None)
    assert loud.loudness_sone > quiet.loudness_sone
    assert loud.annoyance > quiet.annoyance


def test_compute_metrics_handles_too_short_audio():
    audio = np.zeros(100, dtype=np.float32)
    m = compute_metrics(audio, 48000, pa_per_full_scale=None)
    assert m.loudness_sone == 0
    assert m.annoyance == 0


def _make_acoustic(slug: str, audio: np.ndarray, fs: int = 48000, cal_id: str | None = None):
    t = datetime.now(UTC)
    meta = AcousticMeasurementMeta(
        t_start=t,
        t_end=t + timedelta(seconds=1),
        pwm_setpoint=1500,
        mic_serial="X1",
        elevation_deg=0.0,
        half=MeasurementHalf.TOP,
        sample_rate=fs,
        calibration_file_id=cal_id,
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


def test_pa_scaling_flags_absolute_and_raises_loudness():
    audio = _sine(0.1, duration_s=0.5)
    rel = compute_metrics(audio, 48000, pa_per_full_scale=None)
    absolute = compute_metrics(audio, 48000, pa_per_full_scale=3.6394)
    assert rel.absolute is False
    assert absolute.absolute is True
    # Same clip, larger pressure → more sone. Guards against the scalar being dropped.
    assert absolute.loudness_sone > rel.loudness_sone


def test_too_short_audio_still_reports_scale():
    short = np.zeros(100, dtype=np.float32)
    assert compute_metrics(short, 48000, pa_per_full_scale=3.6).absolute is True
    assert compute_metrics(short, 48000, pa_per_full_scale=None).absolute is False


def _legacy_cache_payload(loudness: float = 999.0) -> str:
    """A v1 (pre-Pa-scaling) cache file: bare metrics, no version envelope."""
    return json.dumps({
        "loudness_sone": loudness,
        "sharpness_acum": 9.0,
        "roughness_asper": 9.0,
        "fluctuation_vacil": 0.0,
        "annoyance": 999.0,
        "fluctuation_assumed_zero": True,
    })


def test_cache_load_rejects_unversioned_payload(tmp_path):
    d = tmp_path / "m"
    d.mkdir()
    psy_store.cache_path(d).write_text(_legacy_cache_payload())
    assert psy_store.load(d) is None


def test_cache_load_rejects_older_version(tmp_path):
    d = tmp_path / "m"
    d.mkdir()
    payload = json.loads(_legacy_cache_payload())
    payload["absolute"] = False
    psy_store.cache_path(d).write_text(
        json.dumps({"version": psy_store.CACHE_VERSION - 1, "metrics": payload})
    )
    assert psy_store.load(d) is None


def test_cache_roundtrips_current_version(tmp_path):
    d = tmp_path / "m"
    d.mkdir()
    m = compute_metrics(_sine(0.1, duration_s=0.5), 48000, pa_per_full_scale=3.6394)
    psy_store.save(d, m)
    assert psy_store.load(d) == m


def test_endpoint_recomputes_stale_unversioned_cache(client):
    k = Key(motor="m", propeller="p", shroud="s", notes="n")
    keys_store.create_key(k)
    saved = _make_acoustic(k.slug, _sine(0.1, duration_s=0.5))

    cache = psy_store.cache_path(measurement_dir(k.slug, saved.id))
    cache.write_text(_legacy_cache_payload())

    r = client.get(f"/keys/{k.slug}/measurements/{saved.id}/psychoacoustics")
    assert r.status_code == 200, r.text
    assert r.json()["loudness_sone"] != 999.0
    assert r.json()["loudness_sone"] > 0
    assert json.loads(cache.read_text())["version"] == psy_store.CACHE_VERSION


def test_endpoint_applies_calibration_when_present(client):
    k = Key(motor="m", propeller="p", shroud="s", notes="n")
    keys_store.create_key(k)
    cal_text = '"Sens Factor =-11.2dB, SERNO: 8100111"\n20.0 0.0\n20000.0 0.0\n'
    cal_store.save_calibration("8100111", cal_text, parse_umik_calibration(cal_text))

    audio = _sine(0.1, duration_s=0.5)
    with_cal = _make_acoustic(k.slug, audio, cal_id="8100111")
    without_cal = _make_acoustic(k.slug, audio)

    a = client.get(f"/keys/{k.slug}/measurements/{with_cal.id}/psychoacoustics").json()
    b = client.get(f"/keys/{k.slug}/measurements/{without_cal.id}/psychoacoustics").json()
    assert a["absolute"] is True
    assert b["absolute"] is False
    assert a["loudness_sone"] > b["loudness_sone"]
