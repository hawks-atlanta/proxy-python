import json
from main import app
from src.lib.faker import fake_username, fake_password


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
    response = app.test_client().post("/account/register")
    assert response.status_code == 400
    assert (
        json.loads(response.data)["msg"] == "Invalid JSON data provided in the request"
    )

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
