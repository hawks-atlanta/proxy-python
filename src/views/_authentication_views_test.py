import json
from main import app
from config.soap_client import soap_client
from src.lib.faker import fake_username, fake_password


def test_auth_login_successful() -> None:
    test_data = {"username": fake_username(), "password": fake_password()}

    registration_data = {
        "username": test_data["username"],
        "password": test_data["password"],
    }
    registration_result = soap_client.service.account_register(registration_data)
    assert registration_result.error is False

    login_data = {"username": test_data["username"], "password": test_data["password"]}
    response = app.test_client().post("/auth/login", json=login_data)
    assert response.status_code == 200

    json_response = json.loads(response.data)
    assert json_response["msg"] != ""
    assert json_response["token"] != ""


def test_auth_login_invalid_credentials() -> None:
    data = {"username": "unexistent", "password": "password"}
    response = app.test_client().post("/auth/login", json=data)
    json_response = json.loads(response.data)

    assert response.status_code == 401
    assert json_response["msg"] == "Invalid credentials"


def test_auth_login_missing_fields() -> None:
    data = {"username": "miguel"}
    response = app.test_client().post("/auth/login", json=data)
    assert response.status_code == 400

    data = {"password": "miguel"}
    response = app.test_client().post("/auth/login", json=data)
    assert response.status_code == 400


def test_auth_refresh_missing_token() -> None:
    response = app.test_client().post("/auth/refresh")
    assert response.status_code == 401
    assert json.loads(response.data)["msg"] == "Token is missing"


def test_auth_refresh_not_valid_token() -> None:
    test_data = {"username": fake_username(), "password": fake_password()}
    registration_data = {
        "username": test_data["username"],
        "password": test_data["password"],
    }
    registration_result = soap_client.service.account_register(registration_data)
    assert registration_result.error is False

    login_data = {"username": test_data["username"], "password": test_data["password"]}
    login_response = app.test_client().post("/auth/login", json=login_data)
    login_json_response = json.loads(login_response.data)
    assert login_response.status_code == 200

    jwt = login_json_response["token"]
    not_valid_jwt = jwt + "wrong"
    response = app.test_client().post(
        "/auth/refresh", headers={"Authorization": "Bearer " + not_valid_jwt}
    )
    response_json = json.loads(response.data)

    assert response.status_code == 401
    assert response_json["msg"] != ""


def test_challenge_valid_token() -> None:
    test_data = {"username": fake_username(), "password": fake_password()}
    registration_data = {
        "username": test_data["username"],
        "password": test_data["password"],
    }
    registration_result = soap_client.service.account_register(registration_data)
    assert registration_result.error is False

    login_data = {"username": test_data["username"], "password": test_data["password"]}
    login_response = app.test_client().post("/auth/login", json=login_data)
    login_json_response = json.loads(login_response.data)
    assert login_response.status_code == 200

    jwt = login_json_response["token"]
    response = app.test_client().post(
        "/auth/refresh", headers={"Authorization": "Bearer " + jwt}
    )
    response_json = json.loads(response.data)

    assert response.status_code == 200
    assert response_json["token"] != ""
