from random import randbytes
from main import app

from src.config.soap_client import soap_client
from src.lib.faker import fake_username, fake_password

# RENAME FILE TESTS
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

    # Empty file otherUsername
    response = app.test_client().post(
        "file/share",
        json={"fileUUID": "", "otherUsername": "username123"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400


