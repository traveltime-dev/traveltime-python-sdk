import typing
from datetime import datetime

from typing import List, Optional

from pydantic.main import BaseModel

from traveltimepy import (
    Range,
    PublicTransport,
    Driving,
    Ferry,
    Walking,
    Cycling,
    DrivingTrain,
    CyclingPublicTransport,
)
from traveltimepy.dto.common import CellProperty, Coordinates, H3Centroid, Snapping
from traveltimepy.dto.requests.request import TravelTimeRequest
from traveltimepy.dto.responses.h3 import H3Response
from traveltimepy.itertools import split, flatten


class DepartureSearch(BaseModel):
    id: str
    coords: typing.Union[Coordinates, H3Centroid]
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
    range: Optional[Range]
    snapping: Optional[Snapping]


class ArrivalSearch(BaseModel):
    id: str
    coords: typing.Union[Coordinates, H3Centroid]
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
    range: Optional[Range]
    snapping: Optional[Snapping]


class Intersection(BaseModel):
    id: str
    search_ids: List[str]


class Union(BaseModel):
    id: str
    search_ids: List[str]


class H3Request(TravelTimeRequest[H3Response]):
    resolution: int
    properties: List[CellProperty]
    departure_searches: List[DepartureSearch]
    arrival_searches: List[ArrivalSearch]
    unions: List[Union]
    intersections: List[Intersection]

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        return [
            H3Request(
                resolution=self.resolution,
                properties=self.properties,
                departure_searches=departures,
                arrival_searches=arrivals,
                unions=self.unions,
                intersections=self.intersections,
            )
            for departures, arrivals in split(
                self.departure_searches, self.arrival_searches, window_size
            )
        ]

    def merge(self, responses: List[H3Response]) -> H3Response:
        if len(self.unions) != 0:
            return H3Response(
                results=list(
                    filter(
                        lambda res: res.search_id == "Union search",
                        flatten([response.results for response in responses]),
                    )
                )
            )
        elif len(self.intersections) != 0:
            return H3Response(
                results=list(
                    filter(
                        lambda res: res.search_id == "Intersection search",
                        flatten([response.results for response in responses]),
                    )
                )
            )
        else:
            return H3Response(
                results=sorted(
                    flatten([response.results for response in responses]),
                    key=lambda res: res.search_id,
                )
            )
