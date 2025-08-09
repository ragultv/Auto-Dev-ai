import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Auto-Dev-ai Backend API"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_prompt():
    response = client.post(
        "/api/v1/prompts/",
        json={"prompt": "Create a simple web application"}
    )
    assert response.status_code == 200 