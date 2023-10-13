import typing
from datetime import datetime

from typing import List, Optional

from pydantic.main import BaseModel

from traveltimepy import (
    Coordinates,
    Range,
    PublicTransport,
    Driving,
    Ferry,
    Walking,
    Cycling,
    DrivingTrain,
)
from traveltimepy.dto.requests.request import TravelTimeRequest
from traveltimepy.dto.responses.time_map_wkt import WKTResponseCollection
from traveltimepy.itertools import split, flatten


class DepartureSearch(BaseModel):
    id: str
    coords: Coordinates
    departure_time: datetime
    travel_time: int
    transportation: typing.Union[
        PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain
    ]
    range: Optional[Range] = None


class ArrivalSearch(BaseModel):
    id: str
    coords: Coordinates
    arrival_time: datetime
    travel_time: int
    transportation: typing.Union[
        PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain
    ]
    range: Optional[Range] = None


class TimeMapWKTRequest(TravelTimeRequest[WKTResponseCollection]):
    departure_searches: List[DepartureSearch]
    arrival_searches: List[ArrivalSearch]

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        return [
            TimeMapWKTRequest(
                departure_searches=departures,
                arrival_searches=arrivals
            )
            for departures, arrivals in split(
                self.departure_searches, self.arrival_searches, window_size
            )
        ]

    def merge(self, responses: List[WKTResponseCollection]) -> WKTResponseCollection:
        return WKTResponseCollection(
            results=sorted(
                flatten([response.results for response in responses]),
                key=lambda res: res.search_id,
            )
        )
