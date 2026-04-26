from typing import Optional

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

    def get_all_entities(
            self,
            title: Optional[str] = None,
            verified: Optional[bool] = None,
            page: Optional[int] = None,
            per_page: Optional[int] = None,
    ) -> requests.Response:
        params = {
            key: value
            for key, value in {
                "title": title,
                "verified": verified,
                "page": page,
                "per_page": per_page,
            }.items()
            if value is not None
        }

        return requests.get(
            url=f"{self.base_url}{EntityEndpoints.GET_ALL}",
            params=params,
        )

    def patch_entity(self, entity_id: str | int, payload: dict) -> requests.Response:
        return requests.patch(
            url=f"{self.base_url}{EntityEndpoints.PATCH.format(entity_id=entity_id)}",
            json=payload,
        )

    def delete_entity(self, entity_id: str | int) -> requests.Response:
        return requests.delete(
            url=f"{self.base_url}{EntityEndpoints.DELETE.format(entity_id=entity_id)}",
        )
