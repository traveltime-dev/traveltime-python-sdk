import typing
from datetime import datetime

from typing import List, Optional

from fastkml import KML
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
    LevelOfDetail,
)
from traveltimepy.dto.requests.request import TravelTimeRequest
from traveltimepy.dto.requests.time_map import (
    TimeMapRequest,
    DepartureSearch,
    ArrivalSearch,
)
from traveltimepy.dto.responses.time_map_kml import KMLResponse
from traveltimepy.itertools import split, flatten


class TimeMapRequestKML(TravelTimeRequest[KML]):
    departure_searches: List[DepartureSearch]
    arrival_searches: List[ArrivalSearch]

    def split_searches(self, window_size: int) -> List[TimeMapRequest]:
        return [
            TimeMapRequest(
                departure_searches=departures,
                arrival_searches=arrivals,
            )
            for departures, arrivals in split(
                self.departure_searches, self.arrival_searches, window_size
            )
        ]

    def merge(self, responses: List[KMLResponse]) -> KMLResponse:
        merged_features = flatten([response.placemarks for response in responses])
        return KMLResponse(placemarks=merged_features)
