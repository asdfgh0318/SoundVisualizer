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


def test_defaults_when_file_missing(client):
    r = client.get("/compat-tolerances")
    assert r.status_code == 200
    body = r.json()
    # Defaults from schemas.py
    assert body["thrust_n"]["abs"] == 0.5
    assert body["thrust_n"]["rel"] == 0.05
    assert body["rpm_mean"]["rel"] == 0.02


def test_put_roundtrip(client):
    payload = {
        "thrust_n": {"abs": 1.0, "rel": 0.10},
        "torque_nm": {"abs": 0.10, "rel": 0.15},
        "current_a": {"abs": 1.0, "rel": 0.10},
        "voltage_v": {"abs": 0.5, "rel": 0.0},
        "rpm_mean": {"abs": 200, "rel": 0.05},
    }
    r = client.put("/compat-tolerances", json=payload)
    assert r.status_code == 200, r.text

    r = client.get("/compat-tolerances")
    body = r.json()
    assert body["thrust_n"]["abs"] == 1.0
    assert body["rpm_mean"]["abs"] == 200


def test_negative_rejected(client):
    r = client.put("/compat-tolerances", json={"thrust_n": {"abs": -1.0, "rel": 0.05}})
    assert r.status_code == 422
