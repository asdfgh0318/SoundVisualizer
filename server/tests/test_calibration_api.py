import io

import pytest
from fastapi.testclient import TestClient

from server.main import app


@pytest.fixture(autouse=True)
def _data_dir(tmp_path, monkeypatch):
    monkeypatch.setenv("SOUNDVIS_DATA", str(tmp_path))
    return tmp_path


@pytest.fixture
def client():
    return TestClient(app)


CAL_FILE = b'''"Sens Factor =-1.7240dB, SERNO: 8100123"
"AGain=-9.0dB"
20.0   -0.45
1000.0  0.00
20000.0 -2.10
'''


def test_upload_and_list_calibration(client):
    r = client.post(
        "/calibrations",
        files={"file": ("cal.txt", io.BytesIO(CAL_FILE), "text/plain")},
    )
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["serial"] == "8100123"
    assert body["id"] == "8100123"
    assert body["n_points"] == 3

    r = client.get("/calibrations")
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 1
    assert items[0]["id"] == "8100123"


def test_upload_calibration_with_explicit_serial_overrides_header(client):
    r = client.post(
        "/calibrations?serial=override-99",
        files={"file": ("cal.txt", io.BytesIO(CAL_FILE), "text/plain")},
    )
    assert r.status_code == 201, r.text
    assert r.json()["id"] == "override-99"


def test_upload_calibration_rejects_garbage(client):
    r = client.post(
        "/calibrations",
        files={"file": ("garbage.txt", io.BytesIO(b"not a cal file"), "text/plain")},
    )
    assert r.status_code == 400


def test_list_audio_devices(client):
    r = client.get("/devices/audio")
    assert r.status_code == 200
    devices = r.json()
    # at least the default ALSA device should always be present on a Linux box
    assert isinstance(devices, list)
    for d in devices:
        assert d["max_input_channels"] >= 1
        assert "name" in d
        assert "index" in d
