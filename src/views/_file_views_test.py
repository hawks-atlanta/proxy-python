from uuid import uuid4
from random import randbytes
from config.soap_client import soap_client
from src.lib.faker import fake_username, fake_password

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
    response = soap_client.service.file_check(
        {"token": token, "fileUUID": upload_response.fileUUID}
    )

    # Note that, since the file is saved locally, it will be ready almost instantly
    assert response.code == 200
    assert response.ready is True
    assert response.msg == "File status has been obtained successfully"
