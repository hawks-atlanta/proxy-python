from random import randbytes
from main import app
from uuid import uuid4
from src.config.soap_client import soap_client
from src.lib.faker import fake_username, fake_password

# DOWNLOAD FILE TESTS
download_test_data = {
    "username": fake_username(),
    "password": fake_password(),
    "file": {
        "uuid": None,
        "name": "picture.jpeg",
        "content": randbytes(1024),
    },
}


def test_download_bad_request():
    # Register an user
    register_response = soap_client.service.account_register(
        {
            "username": download_test_data["username"],
            "password": download_test_data["password"],
        }
    )
    assert register_response.error is False

    # Login with the user
    login_response = soap_client.service.auth_login(
        {
            "username": download_test_data["username"],
            "password": download_test_data["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # Unexistent file UUID
    response = app.test_client().get(
        f"/file/download/{uuid4()}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404

    # NO TOKEN
    response = app.test_client().get(
        f"/file/download/{download_test_data['file']['uuid']}"
    )
    assert response.status_code == 401


def test_download_success():
    # Login with the user
    login_response = soap_client.service.auth_login(
        {
            "username": download_test_data["username"],
            "password": download_test_data["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # Upload a file
    create_file_response = soap_client.service.file_upload(
        {
            "token": token,
            "fileName": download_test_data["file"]["name"],
            "fileContent": download_test_data["file"]["content"],
            "location": None,
        }
    )
    assert create_file_response.error is False

    # DOWNLOAD the file
    file_response = app.test_client().get(
        f"/file/download/{create_file_response.fileUUID}",
        headers={"Authorization": f"Bearer {token}"},
    )
    file = file_response.data

    assert file_response.status_code == 200
    assert (
        file_response.headers["Content-Disposition"]
        == f"attachment; filename={download_test_data['file']['name']}"
    )
    assert len(file) == len(download_test_data["file"]["content"])
