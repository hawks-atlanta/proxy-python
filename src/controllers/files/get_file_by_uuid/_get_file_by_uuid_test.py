import json
from random import randbytes
from uuid import uuid4

from main import app
from src.config.soap_client import soap_client
from src.lib.faker import fake_username, fake_password

get_file_test_data = {
    "username": fake_username(),
    "password": fake_password(),
    "directory": {"uuid": None, "name": "directory"},
    "file": {
        "uuid": None,
        "name": "picture.jpeg",
        "content": randbytes(1024),
    },
}


def test_get_file_by_uuid_bad_request():
    # Register test user
    register_response = soap_client.service.account_register(
        {
            "username": get_file_test_data["username"],
            "password": get_file_test_data["password"],
        }
    )
    assert register_response.error is False

    # Login with the user
    login_response = soap_client.service.auth_login(
        {
            "username": get_file_test_data["username"],
            "password": get_file_test_data["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # Not valid file UUID (400 Bad Request)
    response = app.test_client().get(
        "/file/1234",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400


def test_get_file_by_uuid_success():
    # Login with the user
    login_response = soap_client.service.auth_login(
        {
            "username": get_file_test_data["username"],
            "password": get_file_test_data["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # Upload file
    upload_response = soap_client.service.file_upload(
        {
            "token": token,
            "directoryUUID": None,
            "fileName": get_file_test_data["file"]["name"],
            "fileContent": get_file_test_data["file"]["content"],
        }
    )
    assert upload_response.error is False
    get_file_test_data["file"]["uuid"] = upload_response.fileUUID

    # Create directory
    create_directory_response = soap_client.service.file_new_dir(
        {
            "token": token,
            "directoryName": get_file_test_data["directory"]["name"],
        }
    )
    assert create_directory_response.error is False
    get_file_test_data["directory"]["uuid"] = create_directory_response.fileUUID

    # Get file
    response = app.test_client().get(
        f"/file/{get_file_test_data['file']['uuid']}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200

    # Check response
    response_json = json.loads(response.data)
    assert response_json["msg"] == "The file have been obtained successfully"
    assert response_json["file"]["uuid"] == get_file_test_data["file"]["uuid"]
    assert response_json["file"]["name"] == get_file_test_data["file"]["name"]
    assert response_json["file"]["extension"] is None
    assert response_json["file"]["size"] == len(get_file_test_data["file"]["content"])
    assert response_json["file"]["isFile"] is True

    # Get directory
    response = app.test_client().get(
        f"/file/{get_file_test_data['directory']['uuid']}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200

    # Check response
    response_json = json.loads(response.data)
    assert response_json["msg"] == "The file have been obtained successfully"
    assert response_json["file"]["uuid"] == get_file_test_data["directory"]["uuid"]
    assert response_json["file"]["name"] == get_file_test_data["directory"]["name"]
    assert response_json["file"]["extension"] is None
    assert response_json["file"]["size"] == 0
    assert response_json["file"]["isFile"] is False


def test_get_file_by_uuid_not_found():
    # Login with the user
    login_response = soap_client.service.auth_login(
        {
            "username": get_file_test_data["username"],
            "password": get_file_test_data["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # Get file
    response = app.test_client().get(
        f"/file/{uuid4()}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404
