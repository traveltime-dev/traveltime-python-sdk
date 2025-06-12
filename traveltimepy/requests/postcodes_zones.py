from datetime import datetime
from enum import Enum
from typing import List, Union, Optional

from pydantic import BaseModel

from traveltimepy.requests.common import Coordinates, FullRange
from traveltimepy.requests.request import TravelTimeRequest
from traveltimepy.responses.zones import (
    PostcodesDistrictsResponse,
    PostcodesSectorsResponse,
)
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


class ZonesProperty(str, Enum):
    TRAVEL_TIME_REACHABLE = "travel_time_reachable"
    TRAVEL_TIME_ALL = "travel_time_all"
    COVERAGE = "coverage"


class PostcodeFilterArrivalSearch(BaseModel):
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
    properties: List[ZonesProperty]
    reachable_postcodes_threshold: float = 0
    range: Optional[FullRange] = None


class PostcodeFilterDepartureSearch(BaseModel):
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
    properties: List[ZonesProperty]
    reachable_postcodes_threshold: float = 0
    range: Optional[FullRange] = None


class PostcodesSectorsRequest(TravelTimeRequest[PostcodesSectorsResponse]):
    departure_searches: List[PostcodeFilterDepartureSearch]
    arrival_searches: List[PostcodeFilterArrivalSearch]

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        return [
            PostcodesSectorsRequest(
                departure_searches=departures, arrival_searches=arrivals
            )
            for departures, arrivals in split(
                self.departure_searches, self.arrival_searches, window_size
            )
        ]

    def merge(
        self, responses: List[PostcodesSectorsResponse]
    ) -> PostcodesSectorsResponse:
        return PostcodesSectorsResponse(
            results=sorted(
                flatten([response.results for response in responses]),
                key=lambda res: res.search_id,
            )
        )


class PostcodesDistrictsRequest(TravelTimeRequest[PostcodesDistrictsResponse]):
    departure_searches: List[PostcodeFilterDepartureSearch]
    arrival_searches: List[PostcodeFilterArrivalSearch]

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        return [
            PostcodesDistrictsRequest(
                departure_searches=departures, arrival_searches=arrivals
            )
            for departures, arrivals in split(
                self.departure_searches, self.arrival_searches, window_size
            )
        ]

    def merge(
        self, responses: List[PostcodesDistrictsResponse]
    ) -> PostcodesDistrictsResponse:
        return PostcodesDistrictsResponse(
            results=sorted(
                flatten([response.results for response in responses]),
                key=lambda res: res.search_id,
            )
        )
