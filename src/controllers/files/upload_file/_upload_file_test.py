import json
import os
from random import randbytes
from main import app

from src.config.soap_client import soap_client
from src.lib.faker import fake_username, fake_password

upload_file_test_data = {
    "username": fake_username(),
    "password": fake_password(),
    "file": {
        "name": "picture",
        "content": randbytes(1024),
    },
}


def test_file_upload_successful() -> None:
    # Register an user
    register_response = soap_client.service.account_register(
        {
            "username": upload_file_test_data["username"],
            "password": upload_file_test_data["password"],
        }
    )
    assert register_response.error is False

    # Login with the user
    login_response = soap_client.service.auth_login(
        {
            "username": upload_file_test_data["username"],
            "password": upload_file_test_data["password"],
        }
    )
    assert login_response.error is False
    token = login_response.auth.token

    # Write random file to disk
    with open(f"./{upload_file_test_data['file']['name']}.jpeg", "wb") as rf:
        rf.write(upload_file_test_data["file"]["content"])

    # Upload file
    response = app.test_client().post(
        "/file/upload",
        headers={"Authorization": f"Bearer {token}"},
        data={
            "file": (open(f"./{upload_file_test_data['file']['name']}.jpeg", "rb")),
            "location": "",
        },
    )
    json_response = json.loads(response.data)

    assert response.status_code == 201
    assert json_response["msg"] == "The file is being uploaded"
    assert json_response["fileUUID"] is not None

    # Delete file from disk
    os.remove(f"./{upload_file_test_data['file']['name']}.jpeg")
