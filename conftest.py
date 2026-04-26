import pytest

from api.entity.entity_api import EntityApi
from api.entity.models.request_models import AdditionRequest, EntityRequest
from data.data_api import BASE_URL


@pytest.fixture
def base_url() -> str:
    return BASE_URL


@pytest.fixture
def entity_api(base_url: str) -> EntityApi:
    return EntityApi(base_url)


@pytest.fixture
def entity_payload() -> dict:
    payload = EntityRequest(
        addition=AdditionRequest(
            additional_info="Дополнительные сведения",
            additional_number=123,
        ),
        important_numbers=[42, 87, 15],
        title="Заголовок сущности",
        verified=True,
    )
    return payload.model_dump()
