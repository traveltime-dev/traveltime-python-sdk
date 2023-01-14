import typing
from datetime import datetime

from typing import List, Optional

from pydantic.main import BaseModel

from traveltimepy.dto import Coordinates, SearchId
from traveltimepy.dto.requests import Range
from traveltimepy.dto.requests.request import TravelTimeRequest
from traveltimepy.dto.responses.time_map import TimeMapResponse
from traveltimepy.itertools import split, flatten
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


class TimeMapRequest(TravelTimeRequest[TimeMapResponse]):
    departure_searches: List[DepartureSearch]
    arrival_searches: List[ArrivalSearch]
    unions: List[Union]
    intersections: List[Intersection]

    def split_searches(self) -> List[TravelTimeRequest]:
        return [
            TimeMapRequest(
                departure_searches=departures,
                arrival_searches=arrivals,
                unions=self.unions,
                intersections=self.intersections
            )
            for departures, arrivals in split(self.departure_searches, self.arrival_searches, 10)
        ]

    def merge(self, responses: List[TimeMapResponse]) -> TimeMapResponse:
        return TimeMapResponse(results=flatten([response.results for response in responses]))
