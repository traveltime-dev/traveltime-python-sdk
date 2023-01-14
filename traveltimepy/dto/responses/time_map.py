from typing import List

from pydantic.main import BaseModel

from traveltimepy.dto.common import SearchId, Coordinates


class Shape(BaseModel):
    shell: List[Coordinates]
    holes: List[List[Coordinates]]


class Result(BaseModel):
    search_id: SearchId
    shapes: List[Shape]


class TimeMapResponse(BaseModel):
    results: List[Result]
