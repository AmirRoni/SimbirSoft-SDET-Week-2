from api.entity.models.response_models import EntityResponse, CreateEntityResponse, GetAllEntitiesResponse


def assert_entity_matches_payload(entity: EntityResponse, payload: dict):
    assert entity.title == payload["title"], "Заголовок сущности не совпадает"
    assert entity.verified == payload["verified"], "Значение verified не совпадает"
    assert entity.important_numbers == payload["important_numbers"], "Список important_numbers не совпадает"
    assert entity.addition.additional_info == payload["addition"][
        "additional_info"], "Поле additional_info не совпадает"
    assert entity.addition.additional_number == payload["addition"][
        "additional_number"], "Поле additional_number не совпадает"


def test_create_entity(entity_api, entity_payload):
    response = entity_api.create_entity(entity_payload)

    assert response.status_code == 200, (
        f"Ожидался статус 200, получен {response.status_code}"
    )

    create_response = CreateEntityResponse.model_validate(response.text.strip())
    entity_id = create_response.root

    assert entity_id.isdigit(), f"id сущности должен быть числом, получено: {entity_id}"


def test_get_entity_by_id(entity_api, entity_payload, created_entity_id):
    response = entity_api.get_entity(created_entity_id)

    assert response.status_code == 200, (
        f"Ожидался статус 200 при получении сущности, получен {response.status_code}"
    )

    entity = EntityResponse.model_validate(response.json())

    assert str(entity.id) == created_entity_id, (
        "id полученной сущности не совпадает с id созданной сущности"
    )
    assert_entity_matches_payload(entity, entity_payload)


def test_get_all_entities(entity_api, created_entity_id):
    response = entity_api.get_all_entities()

    assert response.status_code == 200, (
        f"Ожидался статус 200 при получении списка сущностей, получен {response.status_code}"
    )

    get_all_response = GetAllEntitiesResponse.model_validate(response.json())
    entities = get_all_response.entity

    assert len(entities) > 0, "Список сущностей не должен быть пустым"
    assert any(str(entity.id) == created_entity_id for entity in entities), (
        "Созданная сущность не найдена в общем списке"
    )


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

    patch_response = entity_api.patch_entity(created_entity_id, updated_payload)

    assert patch_response.status_code == 204, (
        f"Ожидался статус 204 при обновлении сущности, получен {patch_response.status_code}"
    )
    assert patch_response.text == "", "При 204 No Content тело ответа должно быть пустым"

    get_response = entity_api.get_entity(created_entity_id)

    assert get_response.status_code == 200, (
        f"Ожидался статус 200 при получении обновлённой сущности, получен {get_response.status_code}"
    )

    updated_entity = EntityResponse.model_validate(get_response.json())

    assert str(updated_entity.id) == created_entity_id, (
        "id обновлённой сущности не совпадает с id созданной сущности"
    )
    assert_entity_matches_payload(updated_entity, updated_payload)


def test_delete_entity(entity_api, created_entity_id):
    response = entity_api.delete_entity(created_entity_id)

    assert response.status_code == 204, (
        f"Ожидался статус 204 при удалении сущности, получен {response.status_code}"
    )
    assert response.text == "", "При 204 No Content тело ответа должно быть пустым"
