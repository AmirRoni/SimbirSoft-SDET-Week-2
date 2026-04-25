import requests


class EntityApi:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def create_entity(self, payload: dict) -> requests.Response:
        return requests.post(
            f"{self.base_url}/api/create",
            json=payload,
        )
