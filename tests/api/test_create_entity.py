import allure
import pytest

from api.entity.models.response_models import CreateEntityResponse

pytestmark = pytest.mark.xdist_group("entity_api")


@allure.feature("Entity API")
@allure.story("Создание сущности")
@allure.title("Создание сущности через API")
def test_create_entity(entity_api, entity_payload):
    with allure.step("Отправить POST-запрос на создание сущности"):
        response = entity_api.create_entity(entity_payload)

    with allure.step("Проверить статус-код ответа"):
        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}"
        )

    with allure.step("Десериализовать ответ в модель CreateEntityResponse"):
        create_response = CreateEntityResponse.model_validate(response.text.strip())
        entity_id = create_response.root

    with allure.step("Проверить, что в ответе вернулся числовой id"):
        assert entity_id.isdigit(), f"id сущности должен быть числом, получено: {entity_id}"
