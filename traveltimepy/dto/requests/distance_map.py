import typing
from datetime import datetime

from typing import List, Optional

from pydantic.main import BaseModel

from traveltimepy import (
    PublicTransport,
    Driving,
    Ferry,
    Walking,
    Cycling,
    DrivingTrain,
    CyclingPublicTransport,
)
from traveltimepy.dto.common import PolygonsFilter, Snapping, Coordinates, LevelOfDetail
from traveltimepy.dto.requests.request import TravelTimeRequest
from traveltimepy.dto.responses.time_map import TimeMapResponse
from traveltimepy.itertools import split, flatten


class DistanceMapDepartureSearch(BaseModel):
    id: str
    coords: Coordinates
    departure_time: datetime
    travel_distance: int
    transportation: typing.Union[
        PublicTransport,
        Driving,
        Ferry,
        Walking,
        Cycling,
        DrivingTrain,
        CyclingPublicTransport,
    ]
    level_of_detail: Optional[LevelOfDetail] = None
    snapping: Optional[Snapping] = None
    polygons_filter: Optional[PolygonsFilter] = None
    no_holes: Optional[bool] = None


class DistanceMapArrivalSearch(BaseModel):
    id: str
    coords: Coordinates
    arrival_time: datetime
    travel_distance: int
    transportation: typing.Union[
        PublicTransport,
        Driving,
        Ferry,
        Walking,
        Cycling,
        DrivingTrain,
        CyclingPublicTransport,
    ]
    level_of_detail: Optional[LevelOfDetail] = None
    snapping: Optional[Snapping] = None
    polygons_filter: Optional[PolygonsFilter] = None
    no_holes: Optional[bool] = None


class DistanceMapIntersection(BaseModel):
    id: str
    search_ids: List[str]


class DistanceMapUnion(BaseModel):
    id: str
    search_ids: List[str]


class DistanceMapRequest(TravelTimeRequest[TimeMapResponse]):
    departure_searches: List[DistanceMapDepartureSearch]
    arrival_searches: List[DistanceMapArrivalSearch]
    unions: List[DistanceMapUnion]
    intersections: List[DistanceMapIntersection]

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        # Do not split request if unions/intersections are defined
        if len(self.unions) > 0 or len(self.intersections) > 0:
            return [self]
        else:
            chunks = split(self.departure_searches, self.arrival_searches, window_size)

            return [
                DistanceMapRequest(
                    departure_searches=departures,
                    arrival_searches=arrivals,
                    unions=self.unions,
                    intersections=self.intersections,
                )
                for departures, arrivals in chunks
            ]

    def merge(self, responses: List[TimeMapResponse]) -> TimeMapResponse:
        return TimeMapResponse(
            results=sorted(
                flatten([response.results for response in responses]),
                key=lambda res: res.search_id,
            )
        )
