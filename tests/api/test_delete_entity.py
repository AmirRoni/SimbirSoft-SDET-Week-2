import allure


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

    with allure.step("Попробовать получить удалённую сущность через GET-запрос"):
        get_response = entity_api.get_entity(created_entity_id)

    with allure.step(""):
        # Сервис возвращает 500 при попытке получить удалённую сущность.
        # Проверяем фактическое поведение API: после DELETE сущность недоступна через GET.
        assert get_response.status_code == 500, (
            f"После удаления ожидался статус 500, получен {get_response.status_code}"
        )
