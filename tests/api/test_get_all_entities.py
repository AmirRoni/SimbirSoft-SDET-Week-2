import allure
import pytest

from api.entity.models.response_models import GetAllEntitiesResponse

pytestmark = pytest.mark.xdist_group("entity_api")


@allure.feature("Entity API")
@allure.story("Получение списка сущностей")
@allure.title("Получение списка сущностей")
def test_get_all_entities(entity_api, created_entity_id):
    with allure.step("Отправить GET-запрос на получение списка сущностей"):
        response = entity_api.get_all_entities()

    with allure.step("Проверить статус-код ответа"):
        assert response.status_code == 200, (
            f"Ожидался статус 200 при получении списка сущностей, получен {response.status_code}"
        )

    with allure.step("Десериализовать ответ в модель GetAllEntitiesResponse"):
        get_all_response = GetAllEntitiesResponse.model_validate(response.json())
        entities = get_all_response.entity

    with allure.step("Проверить, что список не пустой и содержит созданную сущность"):
        assert len(entities) > 0, "Список сущностей не должен быть пустым"
        assert any(str(entity.id) == created_entity_id for entity in entities), (
            "Созданная сущность не найдена в общем списке"
        )
