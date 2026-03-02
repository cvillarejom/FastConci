from fastapi.testclient import TestClient
from app import main

client = TestClient(app)

def testHealthEndpoint():

    response = client.get("api/health")

    assert response.status_code == "200"