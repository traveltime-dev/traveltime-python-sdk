from datetime import datetime
from typing import List, Optional, Union

from pydantic.main import BaseModel

from traveltimepy.dto.common import Location, Property, FullRange, Snapping
from traveltimepy.dto.transportation import (
    PublicTransport,
    Driving,
    Ferry,
    Walking,
    Cycling,
    DrivingTrain,
    CyclingPublicTransport,
)
from traveltimepy.dto.requests.request import TravelTimeRequest
from traveltimepy.dto.responses.routes import RoutesResponse
from traveltimepy.itertools import split, flatten


class ArrivalSearch(BaseModel):
    id: str
    departure_location_ids: List[str]
    arrival_location_id: str
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
    range: Optional[FullRange]
    snapping: Optional[Snapping]


class DepartureSearch(BaseModel):
    id: str
    arrival_location_ids: List[str]
    departure_location_id: str
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
    range: Optional[FullRange]
    snapping: Optional[Snapping]


class RoutesRequest(TravelTimeRequest[RoutesResponse]):
    locations: List[Location]
    departure_searches: List[DepartureSearch]
    arrival_searches: List[ArrivalSearch]

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        return [
            RoutesRequest(
                locations=self.locations,
                departure_searches=departures,
                arrival_searches=arrivals,
            )
            for departures, arrivals in split(
                self.departure_searches, self.arrival_searches, window_size
            )
        ]

    def merge(self, responses: List[RoutesResponse]) -> RoutesResponse:
        return RoutesResponse(
            results=flatten([response.results for response in responses])
        )
