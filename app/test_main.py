from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_check_server():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Server running"}

def test_scrapping_inexistant():
    response = client.get("/inexistant-Page")
    assert response.status_code == 404
    assert response.json() ==  {"message": "Page inexistant-Page not found"}