import json
import os
from random import randbytes
from main import app

from src.config.soap_client import soap_client
from src.lib.faker import fake_username, fake_password

upload_file_test_data = {
    "username": fake_username(),
    "password": fake_password(),
    "file": {
        "name": "picture.jpeg",
        "content": randbytes(1024),
    },
}


def test_file_upload_bad_request() -> None:
    # Register an user
    register_response = soap_client.service.account_register(
        {
            "username": upload_file_test_data["username"],
            "password": upload_file_test_data["password"],
        }
    )
    assert register_response.error is False

    # Login with the user
    login_response = soap_client.service.auth_login(
        {
            "username": upload_file_test_data["username"],
            "password": upload_file_test_data["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # Write random file to disk
    with open(f"./{upload_file_test_data['file']['name']}", "wb") as rf:
        rf.write(upload_file_test_data["file"]["content"])

    # Upload file with empty form data
    response = app.test_client().post(
        "/file/upload",
        headers={"Authorization": f"Bearer {token}"},
        data={},
    )
    json_response = json.loads(response.data)

    assert response.status_code == 400
    assert json_response["msg"] == "Required fields are missing in form data"

    # Upload file with not valid location UUID
    response = app.test_client().post(
        "/file/upload",
        headers={"Authorization": f"Bearer {token}"},
        data={
            "file": (open(f"./{upload_file_test_data['file']['name']}", "rb")),
            "location": "not-valid-uuid",
        },
    )
    json_response = json.loads(response.data)

    assert response.status_code == 400
    assert json_response["msg"] == "Not valid file location provided"


def test_file_upload_successful() -> None:
    # Login with the user
    login_response = soap_client.service.auth_login(
        {
            "username": upload_file_test_data["username"],
            "password": upload_file_test_data["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # Upload file
    response = app.test_client().post(
        "/file/upload",
        headers={"Authorization": f"Bearer {token}"},
        data={
            "file": (open(f"./{upload_file_test_data['file']['name']}", "rb")),
            "location": "",
        },
    )
    json_response = json.loads(response.data)

    assert response.status_code == 201
    assert json_response["msg"] == "The file is being uploaded"
    assert json_response["fileUUID"] is not None


def test_file_upload_conflict() -> None:
    # Login with the user
    login_response = soap_client.service.auth_login(
        {
            "username": upload_file_test_data["username"],
            "password": upload_file_test_data["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # Upload file
    response = app.test_client().post(
        "/file/upload",
        headers={"Authorization": f"Bearer {token}"},
        data={
            "file": (open(f"./{upload_file_test_data['file']['name']}", "rb")),
            "location": "",
        },
    )
    assert response.status_code == 409

    # Delete file from disk
    os.remove(f"./{upload_file_test_data['file']['name']}")
