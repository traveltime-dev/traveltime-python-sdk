import typing
from datetime import datetime

from typing import List, Optional

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
from traveltimepy.dto.common import PolygonsFilter, RenderMode, Snapping
from traveltimepy.dto.requests.request import TravelTimeRequest
from traveltimepy.dto.responses.time_map import TimeMapResponse
from traveltimepy.itertools import split, flatten


class TimeMapDepartureSearch(BaseModel):
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
    level_of_detail: Optional[LevelOfDetail] = None
    snapping: Optional[Snapping] = None
    polygons_filter: Optional[PolygonsFilter] = None
    remove_water_bodies: Optional[bool] = None
    render_mode: Optional[RenderMode] = None


class TimeMapArrivalSearch(BaseModel):
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
    level_of_detail: Optional[LevelOfDetail] = None
    snapping: Optional[Snapping] = None
    polygons_filter: Optional[PolygonsFilter] = None
    remove_water_bodies: Optional[bool] = None
    render_mode: Optional[RenderMode] = None


class TimeMapIntersection(BaseModel):
    id: str
    search_ids: List[str]


class TimeMapUnion(BaseModel):
    id: str
    search_ids: List[str]


class TimeMapRequest(TravelTimeRequest[TimeMapResponse]):
    departure_searches: List[TimeMapDepartureSearch]
    arrival_searches: List[TimeMapArrivalSearch]
    unions: List[TimeMapUnion]
    intersections: List[TimeMapIntersection]

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        # Do not split request if unions/intersections are defined
        if len(self.unions) > 0 or len(self.intersections) > 0:
            return [self]

        return [
            TimeMapRequest(
                departure_searches=departures,
                arrival_searches=arrivals,
                unions=self.unions,
                intersections=self.intersections,
            )
            for departures, arrivals in split(
                self.departure_searches, self.arrival_searches, window_size
            )
        ]

    def merge(self, responses: List[TimeMapResponse]) -> TimeMapResponse:
        return TimeMapResponse(
            results=sorted(
                flatten([response.results for response in responses]),
                key=lambda res: res.search_id,
            )
        )
