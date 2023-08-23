from main import app

def test_view() -> None:
    response = app.test_client().get("/")
    assert response.status_code == 200