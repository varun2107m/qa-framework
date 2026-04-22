import requests
import logging


class APIClient:
    def __init__(self, base_url, headers=None, timeout=10):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.timeout = timeout

        # Default headers
        self.session.headers.update({
            "Content-Type": "application/json"
        })

        # Override / extend headers if provided
        if headers:
            self.session.headers.update(headers)

    def _log_request(self, method, url, **kwargs):
        logging.info(f"{method} Request → {url}")
        if "params" in kwargs:
            logging.info(f"Query Params → {kwargs['params']}")
        if "json" in kwargs:
            logging.info(f"Payload → {kwargs['json']}")

    def _log_response(self, response):
        logging.info(f"Response [{response.status_code}] → {response.url}")

    def get(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        self._log_request("GET", url, params=params)

        response = self.session.get(url, params=params, timeout=self.timeout)

        self._log_response(response)
        return response

    def post(self, endpoint, payload=None):
        url = f"{self.base_url}{endpoint}"
        self._log_request("POST", url, json=payload)

        response = self.session.post(url, json=payload, timeout=self.timeout)

        self._log_response(response)
        return response

    def put(self, endpoint, payload=None):
        url = f"{self.base_url}{endpoint}"
        self._log_request("PUT", url, json=payload)

        response = self.session.put(url, json=payload, timeout=self.timeout)

        self._log_response(response)
        return response

    def delete(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        self._log_request("DELETE", url)

        response = self.session.delete(url, timeout=self.timeout)

        self._log_response(response)
        return response
    
    