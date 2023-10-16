import json
from random import randbytes
from main import app

from src.config.soap_client import soap_client
from src.lib.faker import fake_username, fake_password

# MOVE FILE TESTS
move_file_test_data = {
    "username": fake_username(),
    "password": fake_password(),
    "file": {
        "uuid": None,
        "targetDirectoryUUID": None,
        "name": "test.txt",
        "content": randbytes(1024),
    },
}


def test_move_file_success():
    # Register a user
    register_response = soap_client.service.account_register(
        {
            "username": move_file_test_data["username"],
            "password": move_file_test_data["password"],
        }
    )
    assert register_response.error is False

    # Login with the user
    login_response = soap_client.service.auth_login(
        {
            "username": move_file_test_data["username"],
            "password": move_file_test_data["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # Create a new directory
    new_directory_name = "test_directory"
    create_dir_response = soap_client.service.file_new_dir(
        {
            "directoryName": new_directory_name,
            "location": None,
            "token": token,
        }
    )
    assert create_dir_response["code"] == 201
    directory_uuid = create_dir_response["fileUUID"]

    move_file_test_data["file"]["targetDirectoryUUID"] = directory_uuid

    # Upload a file
    create_file_response = soap_client.service.file_upload(
        {
            "token": token,
            "fileName": move_file_test_data["file"]["name"],
            "fileContent": move_file_test_data["file"]["content"],
            "location": None,
        }
    )
    assert create_file_response.error is False

    # Move the file to the target directory
    response = app.test_client().patch(
        f"/file/{create_file_response.fileUUID}/move",
        json={"targetDirectoryUUID": directory_uuid},
        headers={"Authorization": f"Bearer {token}"},
    )

    json_response = json.loads(response.data)
    assert response.status_code == 200
    assert json_response["msg"].startswith("The file has been moved")


def test_move_file_bad_request():
    # Login with the user
    login_response = soap_client.service.auth_login(
        {
            "username": move_file_test_data["username"],
            "password": move_file_test_data["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # Missing JSON data
    response = app.test_client().patch(
        f"/file/{move_file_test_data['file']['uuid']}/move",
        headers={"Authorization": f"Bearer {token}"},
        json={},
    )
    assert response.status_code == 400

    # Empty targetDirectoryUUID
    response = app.test_client().patch(
        f"/file/{move_file_test_data['file']['uuid']}/move",
        json={"targetDirectoryUUID": ""},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400

    # Non existent file UUID
    response = app.test_client().patch(
        "/file/1234/move",
        json={"targetDirectoryUUID": "some_directory_uuid"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400


def test_move_file_conflict():
    # Login with the user
    login_response = soap_client.service.auth_login(
        {
            "username": move_file_test_data["username"],
            "password": move_file_test_data["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # Create a new directory
    new_directory_name = "test_directory"
    create_dir_response = soap_client.service.file_new_dir(
        {
            "directoryName": new_directory_name,
            "location": None,
            "token": token,
        }
    )
    assert create_dir_response["code"] == 409
    directory_uuid = create_dir_response["fileUUID"]

    move_file_test_data["file"]["targetDirectoryUUID"] = directory_uuid

    # Upload a file
    create_file_response = soap_client.service.file_upload(
        {
            "token": token,
            "fileName": move_file_test_data["file"]["name"],
            "fileContent": move_file_test_data["file"]["content"],
            "location": None,
        }
    )
    assert create_file_response.error is False

    response = app.test_client().patch(
        f"/file/{create_file_response.fileUUID}/move",
        json={"targetDirectoryUUID": directory_uuid},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400
