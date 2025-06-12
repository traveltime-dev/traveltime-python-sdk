from datetime import datetime
from typing import List, Optional, Union

from pydantic.main import BaseModel

from traveltimepy.requests.common import Location, Property, FullRange, Snapping
from traveltimepy.requests.transportation import (
    PublicTransport,
    Driving,
    Ferry,
    Walking,
    Cycling,
    DrivingTrain,
    CyclingPublicTransport,
)
from traveltimepy.requests.request import TravelTimeRequest
from traveltimepy.responses.routes import RoutesResponse
from traveltimepy.itertools import split, flatten


class RoutesArrivalSearch(BaseModel):
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
    range: Optional[FullRange] = None
    snapping: Optional[Snapping] = None


class RoutesDepartureSearch(BaseModel):
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
    range: Optional[FullRange] = None
    snapping: Optional[Snapping] = None


class RoutesRequest(TravelTimeRequest[RoutesResponse]):
    locations: List[Location]
    departure_searches: List[RoutesDepartureSearch]
    arrival_searches: List[RoutesArrivalSearch]

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
