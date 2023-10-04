import json
from main import app
from config.soap_client import soap_client


def test_auth_login_successful() -> None:
    registration_data = {"username": "miguel3", "password": "miguel3"}

    registration_result = soap_client.service.account_register(registration_data)

    assert registration_result.error is False

    login_data = {"username": "miguel3", "password": "miguel3"}

    response = app.test_client().post("/auth_login", json=login_data)

    assert response.status_code == 200

    assert json.loads(response.data)["message"] == "Login successful"

    assert "token" in json.loads(response.data)


def test_auth_login_invalid_credentials() -> None:
    data = {"username": "miguel1", "password": "miguel"}

    response = app.test_client().post("/auth_login", json=data)

    assert response.status_code == 401

    assert json.loads(response.data)["message"] == "Invalid credentials"


def test_auth_login_missing_fields() -> None:
    data = {"username": "miguel"}

    response = app.test_client().post("/auth_login", json=data)

    assert response.status_code == 400

    assert (
        json.loads(response.data)["message"]
        == "Required fields are missing in JSON data"
    )  # noqa: E501
