import allure

from api.entity.models.response_models import CreateEntityResponse, EntityResponse


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

    with allure.step("Получить созданную сущность через GET-запрос"):
        get_response = entity_api.get_entity(entity_id)

    with allure.step("Проверить статус-код GET-запроса"):
        assert get_response.status_code == 200, (
            f"Ожидался статус 200 при получении созданной сущности, "
            f"получен {get_response.status_code}"
        )

    with allure.step("Десериализовать ответ в модель EntityResponse"):
        created_entity = EntityResponse.model_validate(get_response.json())

    with allure.step("Проверить, что сущность действительно создалась с нужными данными"):
        assert str(created_entity.id) == entity_id, (
            "id полученной сущности не совпадает с id созданной сущности"
        )
