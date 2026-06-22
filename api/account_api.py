from dataclasses import dataclass, asdict
from api.client import ApiClient


@dataclass
class UserData:
    name: str
    email: str
    password: str
    title: str = "Mr"
    birth_date: str = "10"
    birth_month: str = "May"
    birth_year: str = "1990"
    firstname: str = "John"
    lastname: str = "Doe"
    company: str = "TestCompany"
    address1: str = "123 Test Street"
    address2: str = "Apt 4"
    country: str = "United States"
    zipcode: str = "10001"
    state: str = "California"
    city: str = "Los Angeles"
    mobile_number: str = "1234567890"


class AccountApiClient:

    def __init__(self, api_client: ApiClient):
        self._client = api_client

    def create(self, user: UserData) -> dict:

        payload = asdict(user)
        response = self._client.post("/api/createAccount", data=payload)

        assert response.status_code == 200, (
            f"createAccount HTTP-status {response.status_code}, expected 200. "
            f"Responce body: {response.text[:300]}"
        )

        body = response.json()
        assert body.get("responseCode") == 201, (
            f"Account not created, responseCode={body.get('responseCode')}, "
            f"message={body.get('message')}"
        )
        return body

    def delete(self, email: str, password: str) -> dict:
        response = self._client.delete(
            "/api/deleteAccount",
            data={"email": email, "password": password},
        )
        assert response.status_code == 200, (
            f"deleteAccount HTTP-status {response.status_code}"
        )
        return response.json()
