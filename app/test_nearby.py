from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_nearby_empty_params():
    response = client.post(
        "/geo/nearby",
    )
    assert response.status_code == 400


def test_nearby_invalid_params():
    response = client.post(
        "/geo/nearby",
        json={"lat": 999, "lng": 999},
    )
    assert response.status_code == 400


def test_nearby_missing_params():
    response = client.post(
        "/geo/nearby",
        json={"lat": -37},
    )
    assert response.status_code == 400


def test_nearby_ok_params():
    response = client.post(
        "/geo/nearby",
        json={"lat": -37, "lng": 62},
    )
    assert response.status_code == 200
