from datetime import datetime
from typing import List, Union, Optional

from pydantic import BaseModel

from traveltimepy.dto.common import Coordinates, FullRange
from traveltimepy.dto.requests.request import TravelTimeRequest
from traveltimepy.dto.responses.postcodes import PostcodesResponse
from traveltimepy.itertools import split, flatten
from traveltimepy.dto.transportation import PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain
from enum import Enum


class Property(str, Enum):
    TRAVEL_TIME_REACHABLE = 'travel_time_reachable'
    TRAVEL_TIME_ALL = 'travel_time_all'
    COVERAGE = 'coverage'


class ArrivalSearch(BaseModel):
    id: str
    coords: Coordinates
    travel_time: int
    arrival_time: datetime
    transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain]
    properties: List[Property]
    range: Optional[FullRange] = None
    reachable_postcodes_threshold: float


class DepartureSearch(BaseModel):
    id: str
    coords: Coordinates
    travel_time: int
    departure_time: datetime
    transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain]
    properties: List[Property]
    range: Optional[FullRange] = None
    reachable_postcodes_threshold: float


class PostcodesRequest(TravelTimeRequest[PostcodesResponse]):
    departure_searches: List[DepartureSearch]
    arrival_searches: List[ArrivalSearch]

    def split_searches(self) -> List[TravelTimeRequest]:
        return [
            PostcodesRequest(departure_searches=departures, arrival_searches=arrivals)
            for departures, arrivals in split(self.departure_searches, self.arrival_searches, 10)
        ]

    def merge(self, responses: List[PostcodesResponse]) -> PostcodesResponse:
        return PostcodesResponse(
            results=sorted(flatten([response.results for response in responses]), key=lambda res: res.search_id)
        )
