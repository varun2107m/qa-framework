import requests


class APIClient:
    def __init__(self, base_url, timeout=10):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()

    def get(self, endpoint, params=None, headers=None):
        response = self.session.get(
            f"{self.base_url}{endpoint}",
            params=params,
            headers=headers,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response

    def post(self, endpoint, payload=None, headers=None):
        response = self.session.post(
            f"{self.base_url}{endpoint}",
            json=payload,
            headers=headers,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response

    def put(self, endpoint, payload=None, headers=None):
        response = self.session.put(
            f"{self.base_url}{endpoint}",
            json=payload,
            headers=headers,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response

    def delete(self, endpoint, headers=None):
        response = self.session.delete(
            f"{self.base_url}{endpoint}",
            headers=headers,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response

    def get_user(self, user_id):
        return self.get(f"/users/{user_id}")
    
    