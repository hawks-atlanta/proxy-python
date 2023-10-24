from random import randbytes
from main import app
from src.config.soap_client import soap_client
from src.lib.faker import fake_username, fake_password

# SHARED WITH FILE TESTS
shared_files_data = {
    "username": fake_username(),
    "password": fake_password(),
    "otherUsername": fake_username(),
    "file": {
        "uuid": None,
        "name": "picture.jpeg",
        "content": randbytes(1024),
    },
}


def test_shared_bad_request():
    # Register an user
    register_response = soap_client.service.account_register(
        {
            "username": shared_files_data["username"],
            "password": shared_files_data["password"],
        }
    )
    assert register_response.error is False

    # Login with the user
    login_response = soap_client.service.auth_login(
        {
            "username": shared_files_data["username"],
            "password": shared_files_data["password"],
        }
    )
    assert login_response.error is False

    # NO TOKEN
    response = app.test_client().get("/file/shared")
    assert response.status_code == 401


def test_shared_success_request():
    # Register the second user
    register_response2 = soap_client.service.account_register(
        {
            "username": shared_files_data["otherUsername"],
            "password": shared_files_data["password"],
        }
    )
    assert register_response2.error is False

    # Login with the user
    login_response = soap_client.service.auth_login(
        {
            "username": shared_files_data["username"],
            "password": shared_files_data["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # Upload a file as the first user
    upload_response = soap_client.service.file_upload(
        {
            "token": token,
            "fileName": shared_files_data["file"]["name"],
            "fileContent": shared_files_data["file"]["content"],
            "location": None,
        }
    )
    assert upload_response.error is False
    shared_files_data["file"]["uuid"] = upload_response.fileUUID

    # share a file
    create_share_response = soap_client.service.share_file(
        {
            "fileUUID": shared_files_data["file"]["uuid"],
            "otherUsername": shared_files_data["otherUsername"],
            "token": token,
        }
    )
    assert create_share_response.error is False

    login_response2 = soap_client.service.auth_login(
        {
            "username": shared_files_data["otherUsername"],
            "password": shared_files_data["password"],
        }
    )
    assert login_response2.error is False
    token2 = login_response2.auth.token

    # list users
    file_response = app.test_client().get(
        "/file/shared", headers={"Authorization": f"Bearer {token2}"}
    )
    assert file_response.status_code == 200
