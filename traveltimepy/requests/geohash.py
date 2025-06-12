import typing
from datetime import datetime
from typing import List, Optional

from pydantic.main import BaseModel

from traveltimepy.requests.request import TravelTimeRequest
from traveltimepy.requests.transportation import (
    PublicTransport,
    Driving,
    Ferry,
    Walking,
    Cycling,
    DrivingTrain,
    CyclingPublicTransport,
)
from traveltimepy.requests.common import (
    CellProperty,
    Coordinates,
    GeohashCentroid,
    Snapping,
    Range,
)
from traveltimepy.itertools import split, flatten
from traveltimepy.responses.geohash import GeoHashResponse


class GeoHashDepartureSearch(BaseModel):
    id: str
    coords: typing.Union[Coordinates, GeohashCentroid]
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
    snapping: Optional[Snapping] = None


class GeoHashArrivalSearch(BaseModel):
    id: str
    coords: typing.Union[Coordinates, GeohashCentroid]
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
    snapping: Optional[Snapping] = None


class GeoHashIntersection(BaseModel):
    id: str
    search_ids: List[str]


class GeoHashUnion(BaseModel):
    id: str
    search_ids: List[str]


class GeoHashRequest(TravelTimeRequest[GeoHashResponse]):
    resolution: int
    properties: List[CellProperty]
    departure_searches: List[GeoHashDepartureSearch]
    arrival_searches: List[GeoHashArrivalSearch]
    unions: List[GeoHashUnion]
    intersections: List[GeoHashIntersection]

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        # Do not split request if unions/intersections are defined
        if len(self.unions) > 0 or len(self.intersections) > 0:
            return [self]
        else:
            chunks = split(self.departure_searches, self.arrival_searches, window_size)

            return [
                GeoHashRequest(
                    resolution=self.resolution,
                    properties=self.properties,
                    departure_searches=departures,
                    arrival_searches=arrivals,
                    unions=self.unions,
                    intersections=self.intersections,
                )
                for departures, arrivals in chunks
            ]

    def merge(self, responses: List[GeoHashResponse]) -> GeoHashResponse:
        return GeoHashResponse(
            results=sorted(
                flatten([response.results for response in responses]),
                key=lambda res: res.search_id,
            )
        )
