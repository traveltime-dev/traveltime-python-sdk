from datetime import datetime
from typing import List, Union, Optional

from pydantic import BaseModel

from traveltimepy.requests.common import Coordinates, Property, FullRange
from traveltimepy.requests.request import TravelTimeRequest
from traveltimepy.responses.postcodes import PostcodesResponse
from traveltimepy.itertools import split, flatten
from traveltimepy.requests.transportation import (
    PublicTransport,
    Driving,
    Ferry,
    Walking,
    Cycling,
    DrivingTrain,
    CyclingPublicTransport,
)


class PostcodeArrivalSearch(BaseModel):
    id: str
    coords: Coordinates
    travel_time: int
    arrival_time: datetime
    transportation: Union[
        PublicTransport,
        Driving,
        Ferry,
        Walking,
        Cycling,
        DrivingTrain,
        CyclingPublicTransport,
    ]
    properties: List[Property]
    range: Optional[FullRange] = None


class PostcodeDepartureSearch(BaseModel):
    id: str
    coords: Coordinates
    travel_time: int
    departure_time: datetime
    transportation: Union[
        PublicTransport,
        Driving,
        Ferry,
        Walking,
        Cycling,
        DrivingTrain,
        CyclingPublicTransport,
    ]
    properties: List[Property]
    range: Optional[FullRange] = None


class PostcodesRequest(TravelTimeRequest[PostcodesResponse]):
    departure_searches: List[PostcodeDepartureSearch]
    arrival_searches: List[PostcodeArrivalSearch]

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        return [
            PostcodesRequest(departure_searches=departures, arrival_searches=arrivals)
            for departures, arrivals in split(
                self.departure_searches, self.arrival_searches, window_size
            )
        ]

    def merge(self, responses: List[PostcodesResponse]) -> PostcodesResponse:
        return PostcodesResponse(
            results=sorted(
                flatten([response.results for response in responses]),
                key=lambda res: res.search_id,
            )
        )
