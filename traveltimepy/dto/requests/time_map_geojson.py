import typing
from datetime import datetime

from typing import List, Optional

from geojson_pydantic import FeatureCollection
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
    CyclingPublicTransport,
)
from traveltimepy.dto.requests.request import TravelTimeRequest
from traveltimepy.itertools import split, flatten


class DepartureSearch(BaseModel):
    id: str
    coords: Coordinates
    departure_time: datetime
    travel_time: int
    transportation: typing.Union[
        PublicTransport,
        Driving,
        Ferry,
        Walking,
        Cycling,
        DrivingTrain,
        CyclingPublicTransport,
    ]
    range: Optional[Range] = None


class ArrivalSearch(BaseModel):
    id: str
    coords: Coordinates
    arrival_time: datetime
    travel_time: int
    transportation: typing.Union[
        PublicTransport,
        Driving,
        Ferry,
        Walking,
        Cycling,
        DrivingTrain,
        CyclingPublicTransport,
    ]
    range: Optional[Range] = None


class TimeMapRequestGeojson(TravelTimeRequest[FeatureCollection]):
    departure_searches: List[DepartureSearch]
    arrival_searches: List[ArrivalSearch]

    def split_searches(self, window_size: int) -> List[FeatureCollection]:
        return [
            FeatureCollection(
                type="FeatureCollection",
                departure_searches=departures,
                arrival_searches=arrivals,
            )
            for departures, arrivals in split(
                self.departure_searches, self.arrival_searches, window_size
            )
        ]

    def merge(self, responses: List[FeatureCollection]) -> FeatureCollection:
        merged_features = flatten([response.features for response in responses])
        return FeatureCollection(type="FeatureCollection", features=merged_features)
