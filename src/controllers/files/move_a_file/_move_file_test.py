import json
from random import randbytes
from uuid import uuid4

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
    move_file_test_data["file"]["uuid"] = create_file_response.fileUUID

    # Move the file to the target directory
    response = app.test_client().patch(
        f"/file/{move_file_test_data['file']['uuid']}/move",
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
    )
    assert response.status_code == 400

    # Not valid target directory UUID
    response = app.test_client().patch(
        f"/file/{move_file_test_data['file']['uuid']}/move",
        json={"targetDirectoryUUID": "not_valid_uuid"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400

    # Non existent file UUID
    response = app.test_client().patch(
        f"/file/{uuid4()}/move",
        json={"targetDirectoryUUID": uuid4()},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


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

    # Try to move the file to the same directory
    response = app.test_client().patch(
        f"/file/{move_file_test_data['file']['uuid']}/move",
        json={
            "targetDirectoryUUID": move_file_test_data["file"]["targetDirectoryUUID"]
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 409
