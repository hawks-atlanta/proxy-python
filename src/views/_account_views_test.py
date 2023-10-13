import json
from main import app
from src.lib.faker import fake_username, fake_password

register_test_data = {"username": fake_username(), "password": fake_password()}

# REGISTER TEST'S


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


def test_account_password_successful() -> None:
    change_data = {
        "oldpassword": "Andrea1",
        "newpassword": "Andrea2",
        "token": "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTk3NjM1MjcsInV1aWQiOiJjNjU0NmFkMS1jZWFkLTQ5MmYtODkzOS0xY2U0YTc4NzFjMDYifQ.WJV8Qm3KNvr5T_XsHTW2serjTttb93E2GURdNImO0WFwcVBk9BbN8ea1-NPm2rMXEE95EYFc76VaT-kEWt_uZw",
    }
    response = app.test_client().patch("/account/password", json=change_data)

    assert response.status_code == 200
    assert json.loads(response.data)["msg"] == "Password updated successfully"


def test_account_password_missing_fields() -> None:
    # Empty json
    data = {}
    response = app.test_client().patch("/account/password", json=data)

    assert response.status_code == 400
    assert json.loads(response.data)["msg"] == "No JSON data provided in the request"

    # Missing TOKEN
    data = {"oldpassword": "Andrea1", "newpassword": "Andrea2"}
    response = app.test_client().patch("/account/password", json=data)

    assert response.status_code == 400
    assert (
        json.loads(response.data)["msg"] == "Required fields are missing in JSON data"
    )

def test_account_password_not_valid_token() -> None:
    # Empty json
    change_data = {
        "oldpassword": "Andrea1",
        "newpassword": "Andrea2",
        "token": "fghd",
    }
    response = app.test_client().patch("/account/password", json=change_data)

    assert response.status_code == 401
    assert json.loads(response.data)["msg"] == "Unauthorized"

    
