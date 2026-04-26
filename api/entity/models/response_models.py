from pydantic import BaseModel, RootModel


class CreateEntityResponse(RootModel[str]):
    pass


class AdditionResponse(BaseModel):
    id: int
    additional_info: str
    additional_number: int


class EntityResponse(BaseModel):
    id: int
    addition: AdditionResponse
    important_numbers: list[int]
    title: str
    verified: bool


class GetAllEntitiesResponse(BaseModel):
    entity: list[EntityResponse]
