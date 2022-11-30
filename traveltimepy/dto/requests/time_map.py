import typing
from datetime import datetime

from typing import List, Optional

from pydantic.main import BaseModel

from traveltimepy.dto import Coordinates, SearchId
from traveltimepy.dto.requests import Range
from traveltimepy.transportation import PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain


class DepartureSearch(BaseModel):
    id: SearchId
    coords: Coordinates
    departure_time: datetime
    travel_time: int
    transportation: typing.Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain]
    range: Optional[Range] = None


class ArrivalSearch(BaseModel):
    id: SearchId
    coords: Coordinates
    arrival_time: datetime
    travel_time: int
    transportation: typing.Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain]
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
