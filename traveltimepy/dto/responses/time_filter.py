from typing import List, Optional

from pydantic.main import BaseModel

from traveltimepy.dto.common import Route, Fares, SearchId, LocationId


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


class TimeFilterResult(BaseModel):
    search_id: SearchId
    locations: List[Location]
    unreachable: List[LocationId]


class TimeFilterResponse(BaseModel):
    results: List[TimeFilterResult]
