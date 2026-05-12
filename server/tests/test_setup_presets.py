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


SAMPLE_MICS = [
    {"serial": "8100001", "top_elevation_deg": 90, "bottom_elevation_deg": -90,
     "calibration_file_id": None},
    {"serial": "8100002", "top_elevation_deg": 45, "bottom_elevation_deg": -45,
     "calibration_file_id": "8100002"},
]


def test_empty_list(client):
    r = client.get("/setup-presets")
    assert r.status_code == 200
    assert r.json() == []


def test_create_get_delete(client):
    r = client.post("/setup-presets", json={"name": "5-mic-arc", "mics": SAMPLE_MICS})
    assert r.status_code == 201, r.text
    body = r.json()
    preset_id = body["id"]
    assert body["name"] == "5-mic-arc"
    assert len(body["mics"]) == 2

    r = client.get("/setup-presets")
    assert len(r.json()) == 1

    r = client.get(f"/setup-presets/{preset_id}")
    assert r.status_code == 200
    assert r.json()["mics"][0]["serial"] == "8100001"

    r = client.delete(f"/setup-presets/{preset_id}")
    assert r.status_code == 204

    r = client.get(f"/setup-presets/{preset_id}")
    assert r.status_code == 404


def test_empty_name_rejected(client):
    r = client.post("/setup-presets", json={"name": "   ", "mics": SAMPLE_MICS})
    assert r.status_code == 400


def test_most_recent_first(client):
    client.post("/setup-presets", json={"name": "first", "mics": SAMPLE_MICS})
    client.post("/setup-presets", json={"name": "second", "mics": SAMPLE_MICS})
    r = client.get("/setup-presets")
    names = [p["name"] for p in r.json()]
    assert names == ["second", "first"]


def test_delete_missing(client):
    r = client.delete("/setup-presets/nonexistent")
    assert r.status_code == 404
