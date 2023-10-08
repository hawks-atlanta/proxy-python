import json
from main import app
from config.soap_client import soap_client


def test_auth_login_successful() -> None:
    registration_data = {"username": "miguel12", "password": "miguel12"}

    registration_result = soap_client.service.account_register(registration_data)

    assert registration_result.error is False

    login_data = {"username": "miguel12", "password": "miguel12"}

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
    )


def test_auth_refresh_missing_token() -> None:
    # Simulate a request without a token
    data = {"jwt": ""}

    response = app.test_client().post("/auth_refresh", json=data)

    assert response.status_code == 400

    assert json.loads(response.data)["msg"] == "Token is missing in JSON data"


def test_no_valid() -> None:
    registration_data = {"username": "pedro19", "password": "pedro19"}
    registration_result = soap_client.service.account_register(registration_data)
    assert registration_result.error is False

    login_data = {"username": "pedro19", "password": "pedro19"}
    login_response = app.test_client().post("/auth_login", json=login_data)
    assert login_response.status_code == 200
    jwt = json.loads(login_response.data)["jwt"]

    data = {"jwt": jwt + "a"}
    response = app.test_client().post("/auth_refresh", json=data)

    assert response.status_code == 401

    response_data = json.loads(response.data)
    assert "msg" in response_data
    assert response_data["msg"] != ""


def test_challenge_valid_token() -> None:
    registration_data = {"username": "gloria1", "password": "gloria1"}
    registration_result = soap_client.service.account_register(registration_data)
    assert registration_result.error is False

    login_data = {"username": "gloria1", "password": "gloria1"}
    login_response = app.test_client().post("/auth_login", json=login_data)
    assert login_response.status_code == 200
    jwt = json.loads(login_response.data)["jwt"]

    data = {"jwt": jwt}
    response = app.test_client().post("/auth_refresh", json=data)

    assert response.status_code == 200

    # Verificar si la respuesta contiene un token JWT válido
    response_data = json.loads(response.data)
    assert "jwt" in response_data
    assert response_data["jwt"] != ""
