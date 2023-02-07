from typing import List, Optional

from pydantic.main import BaseModel

from traveltimepy.dto.common import Fares


class Property(BaseModel):
    travel_time: int
    fares: Optional[Fares]


class Location(BaseModel):
    id: str
    properties: List[Property]


class RoutesResult(BaseModel):
    search_id: str
    locations: List[Location]
    unreachable: List[str]


class RoutesResponse(BaseModel):
    results: List[RoutesResult]
