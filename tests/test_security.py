def test_missing_api_key_returns_401(unauthorized_client):
    response = unauthorized_client.get("/users/")
    assert response.status_code == 401
    assert response.data["error"] == "Unauthorized"


def test_invalid_api_key_returns_401(unauthorized_client):
    unauthorized_client.credentials(HTTP_X_API_KEY="clave_falsa_123")
    response = unauthorized_client.get("/users/")
    assert response.status_code == 401
