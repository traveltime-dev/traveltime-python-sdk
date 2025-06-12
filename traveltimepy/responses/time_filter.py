from typing import List, Optional

from pydantic.main import BaseModel

from traveltimepy.requests.common import Route, Fares


class DistanceBreakdown(BaseModel):
    mode: str
    distance: int


class TimeFilterProperty(BaseModel):
    travel_time: int
    distance: Optional[int] = None
    distance_breakdown: Optional[List[DistanceBreakdown]] = None
    fares: Optional[Fares] = None
    route: Optional[Route] = None


class Location(BaseModel):
    id: str
    properties: List[TimeFilterProperty]


class TimeFilterResult(BaseModel):
    search_id: str
    locations: List[Location]
    unreachable: List[str]


class TimeFilterResponse(BaseModel):
    results: List[TimeFilterResult]
