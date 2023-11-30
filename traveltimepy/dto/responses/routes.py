from typing import List, Optional

from pydantic.main import BaseModel

from traveltimepy.dto.common import Fares, Route


class Property(BaseModel):
    travel_time: Optional[int] = None
    fares: Optional[Fares] = None
    distance: Optional[int] = None
    route: Optional[Route] = None


class Location(BaseModel):
    id: str
    properties: List[Property]


class RoutesResult(BaseModel):
    search_id: str
    locations: List[Location]
    unreachable: List[str]


class RoutesResponse(BaseModel):
    results: List[RoutesResult]
