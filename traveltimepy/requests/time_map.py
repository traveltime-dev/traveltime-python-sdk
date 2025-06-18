import typing
from datetime import datetime

from typing import List, Optional

from pydantic.main import BaseModel

from traveltimepy.requests.level_of_detail import LevelOfDetail
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
    PolygonsFilter,
    RenderMode,
    Snapping,
    Coordinates,
    Range,
)
from traveltimepy.requests.request import TravelTimeRequest
from traveltimepy.responses.time_map import TimeMapResponse
from traveltimepy.itertools import split, flatten


class TimeMapDepartureSearch(BaseModel):
    """
    Creates travel time catchment area polygons showing all locations reachable
    from a departure point with specific departure time and comprehensive transport options.

    Attributes:
        id: Unique identifier for this search
        coords: Departure point coordinates for the isochrone center
        departure_time: Specific departure time for the journey
        travel_time: Maximum journey time in seconds (max 14,400 = 4 hours)
        transportation: Transportation mode
        range: Optional departure time window for multiple isochrone options
        level_of_detail: Optional polygon detail level for shape complexity
        snapping: Optional road network lookup settings
        polygons_filter: Optional filtering for polygon complexity and size
        remove_water_bodies: Optional flag to exclude water areas from polygons
        render_mode: Optional rendering mode for polygon output optimization
    """

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
    """
    Creates travel time catchment area polygons showing all locations that can
    reach an arrival point with specific arrival time and comprehensive transport options.

    Attributes:
        id: Unique identifier for this search
        coords: Arrival point coordinates for the isochrone center
        arrival_time: Specific arrival time for the journey
        travel_time: Maximum journey time in seconds (max 14,400 = 4 hours)
        transportation: Transportation mode
        range: Optional arrival time window for multiple isochrone options
        level_of_detail: Optional polygon detail level for shape complexity
        snapping: Optional road network lookup settings
        polygons_filter: Optional filtering for polygon complexity and size
        remove_water_bodies: Optional flag to exclude water areas from polygons
        render_mode: Optional rendering mode for polygon output optimization
    """

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
    """
    Defines intersection of multiple isochrone search results.

    Creates a new polygon containing only areas that appear in ALL referenced
    isochrone searches. Useful for finding mutually accessible areas.

    Attributes:
        id: Unique identifier for this intersection
        search_ids: List of search IDs to intersect
    """

    id: str
    search_ids: List[str]


class TimeMapUnion(BaseModel):
    """
    Defines union of multiple isochrone search results.

    Creates a new polygon containing areas that appear in ANY of the referenced
    isochrone searches. Useful for combining multiple catchment areas.

    Attributes:
        id: Unique identifier for this union
        search_ids: List of search IDs to combine
    """

    id: str
    search_ids: List[str]


class TimeMapRequest(TravelTimeRequest[TimeMapResponse]):
    """
    Full-featured isochrone endpoint with comprehensive configurability including
    specific departure/arrival times, range searches, unions, and intersections.

    Attributes:
        departure_searches: List of departure-based isochrone searches (max 10)
        arrival_searches: List of arrival-based isochrone searches (max 10)
        unions: List of union operations combining multiple isochrone results
        intersections: List of intersection operations finding overlapping areas
    """

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
