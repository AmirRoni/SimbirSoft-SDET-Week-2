import allure
import pytest

pytestmark = pytest.mark.xdist_group("entity_api")


@allure.feature("Entity API")
@allure.story("Удаление сущности")
@allure.title("Удаление сущности")
def test_delete_entity(entity_api, created_entity_id):
    with allure.step("Отправить DELETE-запрос на удаление сущности"):
        response = entity_api.delete_entity(created_entity_id)

    with allure.step("Проверить статус-код и пустое тело ответа"):
        assert response.status_code == 204, (
            f"Ожидался статус 204 при удалении сущности, получен {response.status_code}"
        )
        assert response.text == "", "При 204 No Content тело ответа должно быть пустым"
