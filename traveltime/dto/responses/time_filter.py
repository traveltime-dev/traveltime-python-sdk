from typing import List, Optional

from pydantic.main import BaseModel

from traveltime.dto import SearchId, LocationId, Fares
from traveltime.dto.responses import Route


class DistanceBreakdown(BaseModel):
    mode: str
    distance: int


class Property(BaseModel):
    travel_time: int
    distance: Optional[int]
    distance_breakdown: Optional[List[DistanceBreakdown]]
    fares: Optional[Fares]
    route: Optional[Route]


class Location(BaseModel):
    id: LocationId
    properties: List[Property]


class Result(BaseModel):
    search_id: SearchId
    locations: List[Location]
    unreachable: List[LocationId]


class TimeFilterResponse(BaseModel):
    results: List[Result]
