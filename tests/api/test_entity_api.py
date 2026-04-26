from api.entity.models.response_models import EntityResponse, CreateEntityResponse


def test_create_entity(entity_api, entity_payload):
    response = entity_api.create_entity(entity_payload)

    assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
    assert response.text.strip(), "В ответе должен быть id созданной сущности"

    create_response = CreateEntityResponse.model_validate(response.text.strip())
    entity_id = create_response.root
    assert entity_id.isdigit(), f"id сущности должен быть числом, получено: {entity_id}"


def test_get_entity_by_id(entity_api, entity_payload):
    response = entity_api.create_entity(entity_payload)
    assert response.status_code == 200, f"Ожидался статус 200 при создании сущности, получен {response.status_code}"

    create_response = CreateEntityResponse.model_validate(response.text.strip())
    entity_id = create_response.root

    get_response = entity_api.get_entity(entity_id)
    assert get_response.status_code == 200, f"Ожидался статус 200 при получении сущности, получен {get_response.status_code}"

    entity = EntityResponse.model_validate(get_response.json())

    assert str(entity.id) == entity_id, "id полученной сущности не совпадает с id созданной сущности"
    assert entity.title == entity_payload['title'], "Заголовок сущности не совпадает"
    assert entity.verified == entity_payload['verified'], "Значение verified не совпадает"
    assert entity.important_numbers == entity_payload['important_numbers'], "Список important_numbers не совпадает"
    assert entity.addition.additional_info == entity_payload['addition'][
        'additional_info'], "Поле additional_info не совпадает"
    assert entity.addition.additional_number == entity_payload['addition'][
        'additional_number'], "Поле addition_number не совпадает"
