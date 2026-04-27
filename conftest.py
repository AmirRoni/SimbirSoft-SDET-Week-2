import pytest

from api.entity.entity_api import EntityApi
from api.entity.models.response_models import CreateEntityResponse
from data.data_api import BASE_URL
from data.entity_factory import EntityFactory


@pytest.fixture
def base_url() -> str:
    return BASE_URL


@pytest.fixture
def entity_api(base_url: str) -> EntityApi:
    return EntityApi(base_url)


@pytest.fixture
def entity_payload() -> dict:
    return EntityFactory.build_payload()


@pytest.fixture
def created_entity_id(entity_api, entity_payload) -> str:
    response = entity_api.create_entity(entity_payload)

    assert response.status_code == 200, (
        f"Ожидался статус 200 при создании сущности, получен {response.status_code}"
    )

    create_response = CreateEntityResponse.model_validate(response.text.strip())
    entity_id = create_response.root

    assert entity_id.isdigit(), f"id сущности должен быть числом, получено: {entity_id}"

    return entity_id
