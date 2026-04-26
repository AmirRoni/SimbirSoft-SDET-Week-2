import allure
import pytest

from api.entity.models.response_models import EntityResponse
from tests.api.assertions import assert_entity_matches_payload

pytestmark = pytest.mark.xdist_group("entity_api")


@allure.feature("Entity API")
@allure.story("Получение сущности")
@allure.title("Получение сущности по id")
def test_get_entity_by_id(entity_api, entity_payload, created_entity_id):
    with allure.step("Отправить GET-запрос на получение сущности по id"):
        response = entity_api.get_entity(created_entity_id)

    with allure.step("Проверить статус-код ответа"):
        assert response.status_code == 200, (
            f"Ожидался статус 200 при получении сущности, получен {response.status_code}"
        )

    with allure.step("Десериализовать ответ в модель EntityResponse"):
        entity = EntityResponse.model_validate(response.json())

    with allure.step("Проверить id и данные полученной сущности"):
        assert str(entity.id) == created_entity_id, (
            "id полученной сущности не совпадает с id созданной сущности"
        )
        assert_entity_matches_payload(entity, entity_payload)
