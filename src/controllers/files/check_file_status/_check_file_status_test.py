import json
from uuid import uuid4
from random import randbytes
from main import app

from src.config.soap_client import soap_client
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


def test_get_status_bad_request():
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

    # Not valid file UUID (400 Bad Request)
    response = app.test_client().get(
        "/file/1234/status",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400


def test_get_status_not_success_code():
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
