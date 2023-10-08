import json
from main import app
from config.soap_client import soap_client


def test_account_register_successful() -> None:
    register_data = {"username": "andrea", "password": "Andrea1"}

    response = app.test_client().post("/account_register", json=register_data)

    assert response.status_code == 200

    assert json.loads(response.data)["msg"] == "Register succeeded"

    assert "jwt" in json.loads(response.data)


def test_account_register_missing_fields() -> None:
    data = {"username": "andrea"}

    response = app.test_client().post("/account_register", json=data)

    assert response.status_code == 400

    assert (
        json.loads(response.data)["msg"] == "Required fields are missing in JSON data"
    )

def test_account_register_empty_fields() -> None:
    data = {}

    response = app.test_client().post("/account_register", json=data)

    assert response.status_code == 400

    assert (
        json.loads(response.data)["msg"] == "No JSON data provided in the request"
    )


def test_account_register_Username_already_registered() -> None:

    data = {"username": "andrea", "password": "Andrea1"}

    response = app.test_client().post("/account_register", json=data)

    assert response.status_code == 409

    assert json.loads(response.data)["msg"] == "Username already registered"
