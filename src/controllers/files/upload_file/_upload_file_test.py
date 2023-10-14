import json
from main import app


def test_file_upload_successful() -> None:
    file_data = {
        "file": "byte[]",
        "fileName": "picture.png",
        "location": "5295d524-aafc-407c-96ed-adae2cd5047a",
    }
    response = app.test_client().patch("/file/upload", json=file_data)

    assert response.status_code == 201
    assert json.loads(response.data)["msg"] == "File is being uploaded."
