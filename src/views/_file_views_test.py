import json
from uuid import uuid4
from random import randbytes
from main import app
from config.soap_client import soap_client
from src.lib.faker import fake_username, fake_password


# GET STATUS TESTS
get_status_test_data = {
    "username": fake_username(),
    "password": fake_password(),
    "file": {
        "name": "test_file.txt",
        "content": randbytes(1024),
    },
}


def test_get_status_not_success_code():
    # Register an user
    register_response = soap_client.service.account_register(
        {
            "username": get_status_test_data["username"],
            "password": get_status_test_data["password"],
        }
    )
    assert register_response.error is False

    # Login with the user
    login_response = soap_client.service.auth_login(
        {
            "username": get_status_test_data["username"],
            "password": get_status_test_data["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # Try to get status of the file
    random_file_uuid = uuid4()
    response = soap_client.service.file_check(
        {"token": token, "fileUUID": random_file_uuid}
    )

    assert response.code == 404
    assert response.msg == f"There is no file with the {random_file_uuid} UUID"


def test_get_status_success_code():
    # Login with the user
    login_response = soap_client.service.auth_login(
        {
            "username": get_status_test_data["username"],
            "password": get_status_test_data["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # Upload a file
    upload_response = soap_client.service.file_upload(
        {
            "token": token,
            "fileName": get_status_test_data["file"]["name"],
            "fileContent": get_status_test_data["file"]["content"],
            "location": None,
        }
    )
    assert upload_response.error is False

    # Get status of the file
    response = app.test_client().get(
        f"/file/{upload_response.fileUUID}/status",
        headers={"Authorization": f"Bearer {token}"},
    )

    has_expected_success_code = (
        response.status_code == 200 or response.status_code == 202
    )
    assert has_expected_success_code

    json_response = json.loads(response.data)
    has_boolean_ready = (
        json_response["ready"] is True or json_response["ready"] is False
    )
    assert has_boolean_ready

    assert json_response["msg"] == "File status has been obtained successfully"


# RENAME FILE TESTS
rename_test_data = {
    "username": fake_username(),
    "password": fake_password(),
    "file": {
        "uuid": None,
        "name": "test-file",
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
    new_name = "renamed-test-file"
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


# CREATE FOLDER TEST
test_folders = {
    "username": fake_username(),
    "password": fake_password(),
    "folder": {
        "directoryName": "test-directory232",
        "location": "test-location232",
        "token": "test-token232",
    },
}


def test_createfolder_bad_request():
    # Register an user
    register_response = soap_client.service.account_register(
        {
            "username": test_folders["username"],
            "password": test_folders["password"],
        }
    )
    assert register_response.error is False

    # Login with the user
    login_response = soap_client.service.auth_login(
        {
            "username": test_folders["username"],
            "password": test_folders["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # No JSON (400 Bad Request)
    response = app.test_client().post(
        "/folders",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400

    # Empty directory name (400 Bad Request)
    response = app.test_client().post(
        "/folders",
        json={"directoryName": ""},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400


def test_createfolder_success():
    # Login with the user
    login_response = soap_client.service.auth_login(
        {
            "username": test_folders["username"],
            "password": test_folders["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # Create a folder
    create_folder_response = app.test_client().post(
        "/folders",
        json={
            "directoryName": test_folders["folder"]["directoryName"],
            "location": test_folders["folder"]["location"],
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert create_folder_response.status_code == 201


def test_createfolder_duplicate():
    # Login with the user
    login_response = soap_client.service.auth_login(
        {
            "username": test_folders["username"],
            "password": test_folders["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # Create a folder with a duplicate name
    create_folder_response = app.test_client().post(
        "/folders",
        json={
            "directoryName": test_folders["folder"]["directoryName"],
            "location": test_folders["folder"]["location"],
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    # already exists
    assert create_folder_response.status_code == 409
    json.loads(create_folder_response.data)
