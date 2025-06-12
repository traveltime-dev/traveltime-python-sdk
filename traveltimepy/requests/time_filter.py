from datetime import datetime
from typing import List, Optional, Union

from pydantic.main import BaseModel

from traveltimepy.requests.common import Location, FullRange, Property, Snapping
from traveltimepy.requests.request import TravelTimeRequest
from traveltimepy.responses.time_filter import TimeFilterResponse
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


class TimeFilterArrivalSearch(BaseModel):
    id: str
    departure_location_ids: List[str]
    arrival_location_id: str
    arrival_time: datetime
    travel_time: int
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


class TimeFilterDepartureSearch(BaseModel):
    id: str
    arrival_location_ids: List[str]
    departure_location_id: str
    departure_time: datetime
    travel_time: int
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


class TimeFilterRequest(TravelTimeRequest[TimeFilterResponse]):
    locations: List[Location]
    departure_searches: List[TimeFilterDepartureSearch]
    arrival_searches: List[TimeFilterArrivalSearch]

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        return [
            TimeFilterRequest(
                locations=self.locations,
                departure_searches=departures,
                arrival_searches=arrivals,
            )
            for departures, arrivals in split(
                self.departure_searches, self.arrival_searches, window_size
            )
        ]

    def merge(self, responses: List[TimeFilterResponse]) -> TimeFilterResponse:
        return TimeFilterResponse(
            results=flatten([response.results for response in responses])
        )
