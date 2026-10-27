"""Smoke tests for the demo app: both routes answer and include the pod name."""
from app import app


def test_index_reports_pod():
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    # The pod name is what the round-robin demo reads back, so it must be present.
    assert "pod" in resp.get_json()


def test_healthz_ok():
    client = app.test_client()
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"
