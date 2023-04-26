from typing import List, Optional

from pydantic.main import BaseModel

from traveltimepy.dto.common import Fares, Route


class Property(BaseModel):
    travel_time: Optional[int]
    fares: Optional[Fares]
    distance: Optional[int]
    route: Optional[Route]


class Location(BaseModel):
    id: str
    properties: List[Property]


class RoutesResult(BaseModel):
    search_id: str
    locations: List[Location]
    unreachable: List[str]


class RoutesResponse(BaseModel):
    results: List[RoutesResult]
