import typing
from datetime import datetime

from typing import List, Optional

from pydantic.main import BaseModel

from traveltime.dto import Coordinates, SearchId, Range
from traveltime.transportation import Bus, PublicTransport, Driving


class DepartureSearch(BaseModel):
    id: SearchId
    coords: Coordinates
    departure_time: datetime
    travel_time: int
    transportation: typing.Union[Bus, PublicTransport, Driving]
    range: Optional[Range] = None


class ArrivalSearch(BaseModel):
    id: SearchId
    coords: Coordinates
    arrival_time: datetime
    travel_time: int
    transportation: typing.Union[Bus, PublicTransport, Driving]
    range: Optional[Range] = None


class Intersection(BaseModel):
    id: SearchId
    search_ids: List[SearchId]


class Union(BaseModel):
    id: SearchId
    search_ids: List[SearchId]


class TimeMapRequest(BaseModel):
    departure_searches: List[DepartureSearch]
    arrival_searches: List[ArrivalSearch]
    unions: List[Union]
    intersections: List[Intersection]
