from api.entity.models.request_models import AdditionRequest, EntityRequest


class EntityFactory:
    @staticmethod
    def build_payload(
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

    @staticmethod
    def build_updated_payload() -> dict:
        return EntityFactory.build_payload(
            title="Обновлённый заголовок сущности",
            additional_info="Обновлённые дополнительные сведения",
            additional_number=999,
            important_numbers=[10, 20, 30],
            verified=False,
        )
