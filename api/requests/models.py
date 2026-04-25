from typing import List

from pydantic import BaseModel


class AdditionRequest(BaseModel):
    additional_info: str
    additional_number: int


class EntityRequest(BaseModel):
    addition: AdditionRequest
    important_numbers: List[int]
    title: str
    verified: bool
