def test_health_endpoint(client):
    response = client.get("/api/utils/health")

    assert response.status_code == 200