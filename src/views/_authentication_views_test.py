import json
from main import app
from config.soap_client import soap_client


def test_auth_login_successful() -> None:
    registration_data = {"username": "miguel1", "password": "miguel1"}

    registration_result = soap_client.service.account_register(registration_data)

    assert registration_result.error is False

    login_data = {"username": "miguel1", "password": "miguel1"}

    response = app.test_client().post("/auth_login", json=login_data)

    assert response.status_code == 200

    assert json.loads(response.data)["msg"] == "Login successful"

    assert "jwt" in json.loads(response.data)


def test_auth_login_invalid_credentials() -> None:
    data = {"username": "miguel", "password": "miguel"}

    response = app.test_client().post("/auth_login", json=data)

    assert response.status_code == 401

    assert json.loads(response.data)["msg"] == "Invalid credentials"


def test_auth_login_missing_fields() -> None:
    data = {"username": "miguel"}

    response = app.test_client().post("/auth_login", json=data)

    assert response.status_code == 400

    assert (
        json.loads(response.data)["msg"] == "Required fields are missing in JSON data"
    )  # noqa: E501
