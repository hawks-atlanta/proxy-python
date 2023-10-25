from random import randbytes
from main import app
from src.config.soap_client import soap_client
from src.lib.faker import fake_username, fake_password


unshare_files_data = {
    "username": fake_username(),
    "password": fake_password(),
    "otherUsername": fake_username(),
    "file": {
        "uuid": None,
        "name": "picture.jpeg",
        "content": randbytes(1024),
    },
}


def test_unshare_bad_request():
    # Register an user
    register_response = soap_client.service.account_register(
        {
            "username": unshare_files_data["username"],
            "password": unshare_files_data["password"],
        }
    )
    assert register_response.error is False

    # Login with the user
    login_response = soap_client.service.auth_login(
        {
            "username": unshare_files_data["username"],
            "password": unshare_files_data["password"],
        }
    )
    assert login_response.error is False

    # Empty fields in body
    response = app.test_client().post(
        "/file/unshare",
        json={
            "fileUUID": "",
            "otherUsername": "",
        },
        headers={"Authorization": f"Bearer {login_response.auth.token}"},
    )
    assert response.status_code == 400

    # Not valid file UUID
    response = app.test_client().post(
        "/file/unshare",
        json={
            "fileUUID": "not-valid-uuid",
            "otherUsername": unshare_files_data["otherUsername"],
        },
        headers={"Authorization": f"Bearer {login_response.auth.token}"},
    )
    assert response.status_code == 400

    # No body
    response = app.test_client().post(
        "/file/unshare",
        headers={"Authorization": f"Bearer {login_response.auth.token}"},
    )
    assert response.status_code == 400

    # NO TOKEN
    response = app.test_client().post("/file/unshare")
    assert response.status_code == 401


def test_unshare_success_request():
    # Register the second user
    register_response2 = soap_client.service.account_register(
        {
            "username": unshare_files_data["otherUsername"],
            "password": unshare_files_data["password"],
        }
    )
    assert register_response2.error is False

    # Login with the user
    login_response = soap_client.service.auth_login(
        {
            "username": unshare_files_data["username"],
            "password": unshare_files_data["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # Upload a file as the first user
    upload_response = soap_client.service.file_upload(
        {
            "token": token,
            "fileName": unshare_files_data["file"]["name"],
            "fileContent": unshare_files_data["file"]["content"],
            "location": None,
        }
    )
    assert upload_response.error is False
    unshare_files_data["file"]["uuid"] = upload_response.fileUUID

    # share a file
    create_share_response = soap_client.service.share_file(
        {
            "fileUUID": unshare_files_data["file"]["uuid"],
            "otherUsername": unshare_files_data["otherUsername"],
            "token": token,
        }
    )
    assert create_share_response.error is False

    # unshare
    response = app.test_client().post(
        "/file/unshare",
        json={
            "fileUUID": unshare_files_data["file"]["uuid"],
            "otherUsername": unshare_files_data["otherUsername"],
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200

    # Try to unshare the same file again
    response = app.test_client().post(
        "/file/unshare",
        json={
            "fileUUID": unshare_files_data["file"]["uuid"],
            "otherUsername": unshare_files_data["otherUsername"],
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 409
