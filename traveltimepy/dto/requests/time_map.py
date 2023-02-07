import typing
from datetime import datetime

from typing import List, Optional

from pydantic.main import BaseModel

from traveltimepy import Coordinates, Range, PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain
from traveltimepy.dto.requests.request import TravelTimeRequest
from traveltimepy.dto.responses.time_map import TimeMapResponse
from traveltimepy.itertools import split, flatten


class DepartureSearch(BaseModel):
    id: str
    coords: Coordinates
    departure_time: datetime
    travel_time: int
    transportation: typing.Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain]
    range: Optional[Range] = None


class ArrivalSearch(BaseModel):
    id: str
    coords: Coordinates
    arrival_time: datetime
    travel_time: int
    transportation: typing.Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain]
    range: Optional[Range] = None


class Intersection(BaseModel):
    id: str
    search_ids: List[str]


class Union(BaseModel):
    id: str
    search_ids: List[str]


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
        if len(self.unions) != 0:
            print(responses)
            return TimeMapResponse(
                results=list(filter(
                    lambda res: res.search_id == 'Union search',
                    flatten([response.results for response in responses])
                ))
            )
        elif len(self.intersections) != 0:
            return TimeMapResponse(
                results=list(filter(
                    lambda res: res.search_id == 'Intersection search',
                    flatten([response.results for response in responses])
                ))
            )
        else:
            return TimeMapResponse(
                results=sorted(flatten([response.results for response in responses]), key=lambda res: res.search_id)
            )
