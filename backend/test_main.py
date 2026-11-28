from fastapi.testclient import TestClient
from app.main import app
import os
from dotenv import load_dotenv

# API key load karein taaki test fail na ho
load_dotenv()

client = TestClient(app)

def test_health_check():
    """Check karein ki server zinda hai"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_lead():
    """Check karein ki lead ban rahi hai (Mock nahi, asli API call)"""
    payload = {
        "name": "Test User",
        "email": "test@example.com",
        "message": "I want to buy your product urgently.",
        "source": "website"
    }
    response = client.post("/api/v1/leads/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test User"
    assert data["category"] in ["Hot", "Warm", "Cold"]
    assert len(data["reply"]) > 0