from fastapi import FastAPI
from fastapi.testclient import TestClient

def test_minimal():
    app = FastAPI()
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 404
