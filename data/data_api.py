from api.entity.models.request_models import AdditionRequest, EntityRequest


BASE_URL = "http://localhost:8080"


def build_entity_payload(
        title: str = "Заголовок сущности",
        additional_info: str = "Дополнительные сведения",
        additional_number: int = 123,
        important_numbers: list[int] | None = None,
        verified: bool = True,
) -> dict:
    payload = EntityRequest(
        addition=AdditionRequest(
            additional_info=additional_info,
            additional_number=additional_number,
        ),
        important_numbers=important_numbers or [42, 87, 15],
        title=title,
        verified=verified,
    )

    return payload.model_dump()
