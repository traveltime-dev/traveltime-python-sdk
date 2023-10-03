from typing import List

from pydantic.main import BaseModel


class TimeMapWKTResult(BaseModel):
    search_id: str
    shape: str


class TimeMapWKTResponse(BaseModel):
    results: List[TimeMapWKTResult]
