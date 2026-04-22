from services.api_client import APIClient

def test_get_users():
    client = APIClient("https://reqres.in")

    response = client.get("/api/users?page=2")

    assert response.status_code == 200
    