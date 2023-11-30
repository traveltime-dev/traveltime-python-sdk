from typing import List, Optional

from pydantic.main import BaseModel

from traveltimepy.dto.common import Route, Fares


class DistanceBreakdown(BaseModel):
    mode: str
    distance: int


class Property(BaseModel):
    travel_time: int
    distance: Optional[int] = None
    distance_breakdown: Optional[List[DistanceBreakdown]] = None
    fares: Optional[Fares] = None
    route: Optional[Route] = None


class Location(BaseModel):
    id: str
    properties: List[Property]


class TimeFilterResult(BaseModel):
    search_id: str
    locations: List[Location]
    unreachable: List[str]


class TimeFilterResponse(BaseModel):
    results: List[TimeFilterResult]
