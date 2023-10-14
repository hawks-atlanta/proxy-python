import json
from main import app

from src.config.soap_client import soap_client
from src.lib.faker import fake_username, fake_password


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
