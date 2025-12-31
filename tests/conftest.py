import pytest
from django.conf import settings
from rest_framework.test import APIClient


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def api_key():
    return settings.SECRET_KEY


@pytest.fixture
def client(api_key):
    client = APIClient()
    client.credentials(HTTP_X_API_KEY=api_key)
    return client


@pytest.fixture
def unauthorized_client():
    return APIClient()


@pytest.fixture
def sample_user_payload():
    return {
        "name": "Test User",
        "age": 25,
        "music_preferences": ["Rock", "Pop"]
    }


@pytest.fixture
def created_user(client, sample_user_payload):
    response = client.post("/users/", sample_user_payload, format='json')
    assert response.status_code == 201
    return response.data
