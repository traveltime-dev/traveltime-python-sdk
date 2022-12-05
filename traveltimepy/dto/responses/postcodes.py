from typing import List

from pydantic import BaseModel


class Property(BaseModel):
    travel_time: int
    distance: int


class Postcode(BaseModel):
    code: str
    properties: List[Property]


class Result(BaseModel):
    search_id: str
    postcodes: List[Postcode]


class PostcodesResponse(BaseModel):
    results: List[Result]
