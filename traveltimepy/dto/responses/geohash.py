from typing import List, Optional

from pydantic.main import BaseModel


class Properties(BaseModel):
    min: Optional[int] = None
    max: Optional[int] = None
    mean: Optional[int] = None


class Cell(BaseModel):
    id: str
    properties: Properties


class GeohashResult(BaseModel):
    search_id: str
    cells: List[Cell]


class GeohashResponse(BaseModel):
    results: List[GeohashResult]
