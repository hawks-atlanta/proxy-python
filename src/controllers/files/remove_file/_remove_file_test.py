from random import randbytes
from main import app
from uuid import uuid4
from src.config.soap_client import soap_client
from src.lib.faker import fake_username, fake_password


remove_test_data = {
    "username": fake_username(),
    "password": fake_password(),
    "file": {
        "uuid": None,
        "name": "picture.jpeg",
        "content": randbytes(1024),
    },
}


def test_remove_bad_request():
    # Register an user
    register_response = soap_client.service.account_register(
        {
            "username": remove_test_data["username"],
            "password": remove_test_data["password"],
        }
    )
    assert register_response.error is False

    # Login with the user
    login_response = soap_client.service.auth_login(
        {
            "username": remove_test_data["username"],
            "password": remove_test_data["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # Unexistent file UUID
    response = app.test_client().delete(
        f"/file/{uuid4()}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404

    # Not valid file UUID
    response = app.test_client().delete(
        "/file/123",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400

    # NO TOKEN
    response = app.test_client().delete(f"/file/{remove_test_data['file']['uuid']}")
    assert response.status_code == 401


def test_remove_success():
    # Login with the user
    login_response = soap_client.service.auth_login(
        {
            "username": remove_test_data["username"],
            "password": remove_test_data["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # Upload a file
    create_file_response = soap_client.service.file_upload(
        {
            "token": token,
            "fileName": remove_test_data["file"]["name"],
            "fileContent": remove_test_data["file"]["content"],
            "location": None,
        }
    )
    assert create_file_response.error is False

    file_response = app.test_client().delete(
        f"/file/{create_file_response.fileUUID}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert file_response.status_code == 200
