def test_create_entity(entity_api, entity_payload):
    response = entity_api.create_entity(entity_payload)

    assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
    assert response.text.strip(), "В ответе должен быть id созданной сущности"

    entity_id = response.text.strip()
    assert entity_id.isdigit(), f"id сущности должен быть числом, получено: {entity_id}"
