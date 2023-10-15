from random import randbytes
from main import app

from src.config.soap_client import soap_client
from src.lib.faker import fake_username, fake_password

# SHARE FILE TESTS
share_test_data = {
    "username": fake_username(),
    "password": fake_password(),
    "otherUsername": fake_username(),
    "otherPassword": fake_password(),
    "file": {
        "uuid": None,
        "name": "picture.jpeg",
        "content": randbytes(1024),
    },
}


def test_share_bad_request():
    # Register an user
    register_response1 = soap_client.service.account_register(
        {
            "username": share_test_data["username"],
            "password": share_test_data["password"],
        }
    )
    assert register_response1.error is False

    # Login with the one user
    login_response = soap_client.service.auth_login(
        {
            "username": share_test_data["username"],
            "password": share_test_data["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # No token
    response = app.test_client().post(
        "file/share",
    )
    assert response.status_code == 401

    # Empty fields
    response = app.test_client().post(
        "file/share",
        json={"fileUUID": "", "otherUsername": "username123"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400

    # Not valid UUID
    response = app.test_client().post(
        "file/share",
        json={"fileUUID": "not-valid-uuid", "otherUsername": "username123"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400


def test_share_forbidden():
    # Login as the first user
    login_response = soap_client.service.auth_login(
        {
            "username": share_test_data["username"],
            "password": share_test_data["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # Upload a file as the first user
    upload_response = soap_client.service.file_upload(
        {
            "token": token,
            "fileName": share_test_data["file"]["name"],
            "fileContent": share_test_data["file"]["content"],
            "location": None,
        }
    )
    assert upload_response.error is False
    share_test_data["file"]["uuid"] = upload_response.fileUUID

    # Register the second user
    register_response2 = soap_client.service.account_register(
        {
            "username": share_test_data["otherUsername"],
            "password": share_test_data["otherPassword"],
        }
    )
    assert register_response2.error is False

    # Login as the second user
    login_response = soap_client.service.auth_login(
        {
            "username": share_test_data["otherUsername"],
            "password": share_test_data["otherPassword"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # Try to share the file as the second user
    response = app.test_client().post(
        "file/share",
        json={
            "fileUUID": share_test_data["file"]["uuid"],
            "otherUsername": share_test_data["username"],
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403


def test_share_success():
    # Login as the first user
    login_response = soap_client.service.auth_login(
        {
            "username": share_test_data["username"],
            "password": share_test_data["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # Share the file as the first user
    response = app.test_client().post(
        "file/share",
        json={
            "fileUUID": share_test_data["file"]["uuid"],
            "otherUsername": share_test_data["otherUsername"],
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json["msg"] == "File shared successfully"
