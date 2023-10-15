import json
from random import randbytes
from main import app

from src.config.soap_client import soap_client
from src.lib.faker import fake_username, fake_password

list_files_test_data = {
    "owner_username": fake_username(),
    "second_username": fake_username(),
    "password": fake_password(),
    "directory": {"uuid": None, "name": "directory"},
    "file": {
        "uuid": None,
        "name": "picture.jpeg",
        "content": randbytes(1024),
    },
    "nested_file": {
        "uuid": None,
        "name": "nested_picture.jpeg",
        "content": randbytes(1024),
    },
}


def test_list_files_bad_request():
    # Register the users
    register_response = soap_client.service.account_register(
        {
            "username": list_files_test_data["owner_username"],
            "password": list_files_test_data["password"],
        }
    )
    assert register_response.error is False

    register_response = soap_client.service.account_register(
        {
            "username": list_files_test_data["second_username"],
            "password": list_files_test_data["password"],
        }
    )
    assert register_response.error is False

    # Login with the registered user
    login_response = soap_client.service.auth_login(
        {
            "username": list_files_test_data["owner_username"],
            "password": list_files_test_data["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # Send a request with no token
    response = app.test_client().get("/file/list")
    assert response.status_code == 401

    # Send a request with not valid directoryUUID
    response = app.test_client().get(
        "/file/list?directoryUUID=not_valid_uuid",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400


def test_list_files_success():
    # Login with the owner user
    login_response = soap_client.service.auth_login(
        {
            "username": list_files_test_data["owner_username"],
            "password": list_files_test_data["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # Upload a file in the root directory
    upload_response = soap_client.service.file_upload(
        {
            "fileName": list_files_test_data["file"]["name"],
            "fileContent": list_files_test_data["file"]["content"],
            "location": None,
            "token": token,
        }
    )
    assert upload_response.error is False
    list_files_test_data["file"]["uuid"] = upload_response.fileUUID

    # Create a directory in the root directory
    create_dir_response = soap_client.service.file_new_dir(
        {
            "directoryName": list_files_test_data["directory"]["name"],
            "location": None,
            "token": token,
        }
    )
    assert create_dir_response.error is False
    list_files_test_data["directory"]["uuid"] = create_dir_response.fileUUID

    # Upload a file in the created directory
    upload_response = soap_client.service.file_upload(
        {
            "fileName": list_files_test_data["nested_file"]["name"],
            "fileContent": list_files_test_data["nested_file"]["content"],
            "location": list_files_test_data["directory"]["uuid"],
            "token": token,
        }
    )
    assert upload_response.error is False
    list_files_test_data["nested_file"]["uuid"] = upload_response.fileUUID

    # List the files in the root directory
    response = app.test_client().get(
        "/file/list", headers={"Authorization": f"Bearer {token}"}
    )
    response_json = json.loads(response.data)

    assert response.status_code == 200
    assert response_json["msg"] == "Files have been listed successfully"
    assert len(response_json["files"]) == 2

    # List the files in the created directory
    response = app.test_client().get(
        f"/file/list?directoryUUID={list_files_test_data['directory']['uuid']}",
        headers={"Authorization": f"Bearer {token}"},
    )
    response_json = json.loads(response.data)

    assert response.status_code == 200
    assert response_json["msg"] == "Files have been listed successfully"
    assert len(response_json["files"]) == 1


def test_list_files_forbidden():
    # Login with the second user
    login_response = soap_client.service.auth_login(
        {
            "username": list_files_test_data["second_username"],
            "password": list_files_test_data["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # List the files in the created directory
    response = app.test_client().get(
        f"/file/list?directoryUUID={list_files_test_data['directory']['uuid']}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403
