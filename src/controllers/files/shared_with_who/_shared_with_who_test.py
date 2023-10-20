from random import randbytes
from uuid import uuid4
from main import app
from src.config.soap_client import soap_client
from src.lib.faker import fake_username, fake_password

# SHARED WITH FILE TESTS
shared_with_who_test_data = {
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


def test_shared_with_who_bad_request():
    # Register an user
    register_response = soap_client.service.account_register(
        {
            "username": shared_with_who_test_data["username"],
            "password": shared_with_who_test_data["password"],
        }
    )
    assert register_response.error is False

    # Login with the user
    login_response = soap_client.service.auth_login(
        {
            "username": shared_with_who_test_data["username"],
            "password": shared_with_who_test_data["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # Unexistent file UUID
    response = app.test_client().get(
        f"/file/{123}/shared-with-who",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400

    # NO TOKEN
    response = app.test_client().get(
        f"/file/{shared_with_who_test_data['file']['uuid']}/shared-with-who"
    )
    assert response.status_code == 401

def test_shared_with_who_success():
    # Register the second user
    register_response2 = soap_client.service.account_register(
        {
            "username": shared_with_who_test_data["otherUsername"],
            "password": shared_with_who_test_data["otherPassword"],
        }
    )
    assert register_response2.error is False

    # Login with the user
    login_response = soap_client.service.auth_login(
        {
            "username": shared_with_who_test_data["username"],
            "password": shared_with_who_test_data["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # Upload a file as the first user
    upload_response = soap_client.service.file_upload(
        {
            "token": token,
            "fileName": shared_with_who_test_data["file"]["name"],
            "fileContent": shared_with_who_test_data["file"]["content"],
            "location": None,
        }
    )
    assert upload_response.error is False
    shared_with_who_test_data["file"]["uuid"] = upload_response.fileUUID

    # share a file
    create_share_response = soap_client.service.share_file(
        {
            "fileUUID": shared_with_who_test_data["file"]["uuid"],
            "otherUsername": shared_with_who_test_data["otherUsername"],
            "token": token,
        }
    )
    assert create_share_response.error is False

    # list users
    file_response = app.test_client().get(
        f"/file/{shared_with_who_test_data['file']['uuid']}/shared-with-who",
        headers={"Authorization": f"Bearer {token}"},
    )
    json_response = file_response.get_json()

    assert file_response.status_code == 200
    assert len(json_response["users"]) == 1
    assert json_response["users"][0] == shared_with_who_test_data["otherUsername"]

def test_shared_with_who_not_found():
    # Login with the user
    login_response = soap_client.service.auth_login(
        {
            "username": shared_with_who_test_data["username"],
            "password": shared_with_who_test_data["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # Unexistent file UUID
    response = app.test_client().get(
        f"/file/{uuid4()}/shared-with-who",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404