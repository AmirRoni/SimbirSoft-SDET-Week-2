import allure
import pytest

from api.entity.models.response_models import EntityResponse
from tests.api.assertions import assert_entity_matches_payload

pytestmark = pytest.mark.xdist_group("entity_api")


@allure.feature("Entity API")
@allure.story("Обновление сущности")
@allure.title("Обновление сущности через PATCH")
def test_patch_entity(entity_api, created_entity_id):
    updated_payload = {
        "addition": {
            "additional_info": "Обновлённые дополнительные сведения",
            "additional_number": 999,
        },
        "important_numbers": [10, 20, 30],
        "title": "Обновлённый заголовок сущности",
        "verified": False,
    }

    with allure.step("Отправить PATCH-запрос на обновление сущности"):
        patch_response = entity_api.patch_entity(created_entity_id, updated_payload)

    with allure.step("Проверить статус-код и пустое тело ответа"):
        assert patch_response.status_code == 204, (
            f"Ожидался статус 204 при обновлении сущности, получен {patch_response.status_code}"
        )
        assert patch_response.text == "", "При 204 No Content тело ответа должно быть пустым"

    with allure.step("Получить обновлённую сущность"):
        get_response = entity_api.get_entity(created_entity_id)

    with allure.step("Проверить статус-код ответа на GET-запрос"):
        assert get_response.status_code == 200, (
            f"Ожидался статус 200 при получении обновлённой сущности, получен {get_response.status_code}"
        )

    with allure.step("Десериализовать ответ в модель EntityResponse"):
        updated_entity = EntityResponse.model_validate(get_response.json())

    with allure.step("Проверить, что данные сущности обновились"):
        assert str(updated_entity.id) == created_entity_id, (
            "id обновлённой сущности не совпадает с id созданной сущности"
        )
        assert_entity_matches_payload(updated_entity, updated_payload)
