import requests

from api.entity.endpoints import EntityEndpoints


class EntityApi:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def create_entity(self, payload: dict) -> requests.Response:
        return requests.post(
            url=f"{self.base_url}{EntityEndpoints.CREATE}",
            json=payload,
        )

    def get_entity(self, entity_id: str | int) -> requests.Response:
        return requests.get(
            url=f"{self.base_url}{EntityEndpoints.GET_BY_ID.format(entity_id=entity_id)}",
        )
