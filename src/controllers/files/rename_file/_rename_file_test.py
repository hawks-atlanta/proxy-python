import json
from random import randbytes
from main import app

from src.config.soap_client import soap_client
from src.lib.faker import fake_username, fake_password

# RENAME FILE TESTS
rename_test_data = {
    "username": fake_username(),
    "password": fake_password(),
    "file": {
        "uuid": None,
        "name": "test.txt",
        "content": randbytes(1024),
    },
}


def test_rename_bad_request():
    # Register an user
    register_response = soap_client.service.account_register(
        {
            "username": rename_test_data["username"],
            "password": rename_test_data["password"],
        }
    )
    assert register_response.error is False

    # Login with the user
    login_response = soap_client.service.auth_login(
        {
            "username": rename_test_data["username"],
            "password": rename_test_data["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # No JSON
    response = app.test_client().patch(
        f"/file/{rename_test_data['file']['uuid']}/rename",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400

    # Empty file name
    response = app.test_client().patch(
        f"/file/{rename_test_data['file']['uuid']}/rename",
        json={"newName": ""},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400

    # Not valid file UUID
    response = app.test_client().patch(
        "/file/1234/rename",
        json={"newName": "test.txt"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400


def test_rename_success():
    # Login with the user
    login_response = soap_client.service.auth_login(
        {
            "username": rename_test_data["username"],
            "password": rename_test_data["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # Upload a file
    create_file_response = soap_client.service.file_upload(
        {
            "token": token,
            "fileName": rename_test_data["file"]["name"],
            "fileContent": rename_test_data["file"]["content"],
            "location": None,
        }
    )
    assert create_file_response.error is False

    # Rename the file
    new_name = "renamed.txt"
    response = app.test_client().patch(
        f"/file/{create_file_response.fileUUID}/rename",
        json={"newName": new_name},
        headers={"Authorization": f"Bearer {token}"},
    )

    json_response = json.loads(response.data)
    assert response.status_code == 200
    assert json_response["msg"] == "The file has been renamed successfully"

    # Update the test data
    rename_test_data["file"]["uuid"] = create_file_response.fileUUID
    rename_test_data["file"]["name"] = new_name


def test_rename_conflict():
    # Login with the user
    login_response = soap_client.service.auth_login(
        {
            "username": rename_test_data["username"],
            "password": rename_test_data["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # Try to rename the file with the same name
    response = app.test_client().patch(
        f"/file/{rename_test_data['file']['uuid']}/rename",
        json={"newName": rename_test_data["file"]["name"]},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 409
