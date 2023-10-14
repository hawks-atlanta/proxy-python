import json
from main import app
from config.soap_client import soap_client
from src.lib.faker import fake_username, fake_password


# REGISTER TEST'S
register_test_data = {"username": fake_username(), "password": fake_password()}


def test_account_register_successful() -> None:
    register_data = {
        "username": register_test_data["username"],
        "password": register_test_data["password"],
    }
    response = app.test_client().post("/account/register", json=register_data)
    json_response = json.loads(response.data)

    assert response.status_code == 200
    assert json.loads(response.data)["msg"] == "Register succeeded"
    assert json_response["token"] != ""


def test_account_register_missing_fields() -> None:
    # Empty json
    data = {}
    response = app.test_client().post("/account/register", json=data)

    assert response.status_code == 400
    assert json.loads(response.data)["msg"] == "No JSON data provided in the request"

    # Missing password
    data = {"username": register_test_data["username"]}
    response = app.test_client().post("/account/register", json=data)

    assert response.status_code == 400
    assert (
        json.loads(response.data)["msg"] == "Required fields are missing in JSON data"
    )


def test_account_register_Username_already_registered() -> None:
    data = {
        "username": register_test_data["username"],
        "password": register_test_data["password"],
    }
    response = app.test_client().post("/account/register", json=data)
    json_response = json.loads(response.data)

    assert response.status_code == 409
    assert json_response["msg"] == "Username already registered"


# PASSWORD UPDATE TEST'S
update_password_test_data = {"username": fake_username(), "password": fake_password()}


def test_update_password_success() -> None:
    # Register test user
    register_response = soap_client.service.account_register(
        {
            "username": update_password_test_data["username"],
            "password": update_password_test_data["password"],
        }
    )
    assert register_response.error is False

    # Login with the user
    login_response = soap_client.service.auth_login(
        {
            "username": update_password_test_data["username"],
            "password": update_password_test_data["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # Update the password
    change_data = {
        "oldPassword": update_password_test_data["password"],
        "newPassword": "Andrea2",
    }
    response = app.test_client().patch(
        "/account/password",
        json=change_data,
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200
    assert json.loads(response.data)["msg"] == "Password updated successfully"
    update_password_test_data["password"] = change_data["newPassword"]


def test_update_password_missing_fields() -> None:
    # Login with the user
    login_response = soap_client.service.auth_login(
        {
            "username": update_password_test_data["username"],
            "password": update_password_test_data["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # No JSON
    response = app.test_client().patch(
        "/account/password", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400
    assert (
        json.loads(response.data)["msg"] == "Invalid JSON data provided in the request"
    )

    # Missing fields
    data = {}
    response = app.test_client().patch(
        "/account/password",
        json=data,
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 400
    assert (
        json.loads(response.data)["msg"] == "Required fields are missing in JSON data"
    )


def test_update_password_not_valid_token() -> None:
    change_data = {"oldPassword": "Andrea1", "newPassword": "Andrea2"}
    response = app.test_client().patch(
        "/account/password",
        json=change_data,
        headers={
            "Authorization": "Bearer 123",
        },
    )

    assert response.status_code == 401
    assert json.loads(response.data)["msg"] == "unauthorized"
