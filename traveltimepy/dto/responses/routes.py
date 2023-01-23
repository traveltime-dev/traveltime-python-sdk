from typing import List, Optional

from pydantic.main import BaseModel

from traveltimepy.dto.common import SearchId, LocationId, Fares


class Property(BaseModel):
    travel_time: int
    fares: Optional[Fares]


class Location(BaseModel):
    id: LocationId
    properties: List[Property]


class RoutesResult(BaseModel):
    search_id: SearchId
    locations: List[Location]
    unreachable: List[LocationId]


class RoutesResponse(BaseModel):
    results: List[RoutesResult]
