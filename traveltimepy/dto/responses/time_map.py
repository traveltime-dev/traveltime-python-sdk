from typing import List

from pydantic.main import BaseModel

from traveltimepy.dto.common import Coordinates


class Shape(BaseModel):
    shell: List[Coordinates]
    holes: List[List[Coordinates]]


class TimeMapResult(BaseModel):
    search_id: str
    shapes: List[Shape]


class TimeMapResponse(BaseModel):
    results: List[TimeMapResult]
