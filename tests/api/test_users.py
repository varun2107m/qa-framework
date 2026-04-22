from services.api_client import APIClient


def test_get_users():
    client = APIClient("https://jsonplaceholder.typicode.com")

    response = client.get("/users")

    assert response.status_code == 200
    assert len(response.json()) > 0
    