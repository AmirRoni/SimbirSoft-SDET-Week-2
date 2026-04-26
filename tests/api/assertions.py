from api.entity.models.response_models import EntityResponse


def assert_entity_matches_payload(entity: EntityResponse, payload: dict):
    assert entity.title == payload["title"], "Заголовок сущности не совпадает"
    assert entity.verified == payload["verified"], "Значение verified не совпадает"
    assert entity.important_numbers == payload["important_numbers"], "Список important_numbers не совпадает"
    assert entity.addition.additional_info == payload["addition"]["additional_info"], \
        "Поле additional_info не совпадает"
    assert entity.addition.additional_number == payload["addition"]["additional_number"], \
        "Поле additional_number не совпадает"
