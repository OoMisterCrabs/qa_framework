import requests


class ApiClient:

    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def post(self, path: str, data: dict | None = None) -> requests.Response:
        url = f"{self.base_url}{path}"
        return self.session.post(url, data=data, timeout=self.timeout)

    def delete(self, path: str, data: dict | None = None) -> requests.Response:
        url = f"{self.base_url}{path}"
        return self.session.delete(url, data=data, timeout=self.timeout)

    def get(self, path: str, params: dict | None = None) -> requests.Response:
        url = f"{self.base_url}{path}"
        return self.session.get(url, params=params, timeout=self.timeout)
