import json

from main import app
from src.config.soap_client import soap_client
from src.lib.faker import fake_username, fake_password


# CREATE FOLDER TEST
test_folders = {
    "username": fake_username(),
    "password": fake_password(),
    "folder": {
        "uuid": None,
        "directoryName": "test-directory232",
        "location": None,
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

    # Not valid location (400 Bad Request)
    response = app.test_client().post(
        "/folders",
        json={
            "directoryName": test_folders["folder"]["directoryName"],
            "location": "not-valid-uuid",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400


def test_create_folder_in_root_success():
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
    create_folder_json_response = json.loads(create_folder_response.data)

    assert create_folder_response.status_code == 201
    test_folders["folder"]["uuid"] = create_folder_json_response["directoryUUID"]


def test_create_folder_in_folder_success():
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
            "location": test_folders["folder"]["uuid"],
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert create_folder_response.status_code == 201


def test_create_folder_duplicate():
    # Login with the user
    login_response = soap_client.service.auth_login(
        {
            "username": test_folders["username"],
            "password": test_folders["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # Create a folder in root with same name
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

    # Create a folder in folder with same name
    create_folder_response = app.test_client().post(
        "/folders",
        json={
            "directoryName": test_folders["folder"]["directoryName"],
            "location": test_folders["folder"]["uuid"],
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert create_folder_response.status_code == 409
