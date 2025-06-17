from typing import List, Optional

from pydantic import BaseModel, field_serializer

from traveltimepy.requests.common import (
    Coordinates,
    PolygonsFilter,
    RenderMode,
    Snapping,
    ArrivalTimePeriod,
)
from traveltimepy.requests.level_of_detail import LevelOfDetail
from traveltimepy.requests.request import TravelTimeRequest
from traveltimepy.responses.time_map import TimeMapResponse
from traveltimepy.itertools import split, flatten
from traveltimepy.requests.time_filter_fast import TransportationFast


class TimeMapFastSearch(BaseModel):
    """
    Creates travel time catchment areas (isochrones) showing all locations reachable
    within specified travel time. Optimized for speed with limited configurability.

    Attributes:
        id: Unique identifier for this search
        coords: Center point coordinates for the isochrone
        transportation: Transportation mode
        travel_time: Maximum journey time in seconds (max 10,800 = 3 hours)
        arrival_time_period: Time period instead of specific time
        level_of_detail: Optional polygon detail level (simple/coarse_grid)
        snapping: Optional road network lookup settings
        polygons_filter: Optional filtering for polygon complexity
        render_mode: Optional rendering mode for polygon output
    """

    id: str
    coords: Coordinates
    transportation: TransportationFast
    travel_time: int
    arrival_time_period: ArrivalTimePeriod = ArrivalTimePeriod.WEEKDAY_MORNING
    level_of_detail: Optional[LevelOfDetail] = None
    snapping: Optional[Snapping] = None
    polygons_filter: Optional[PolygonsFilter] = None
    render_mode: Optional[RenderMode] = None

    # JSON expects `"transportation": { "type": "public_transport" }` and not `"transportation": "public_transport"`
    @field_serializer("transportation")
    def serialize_transportation(self, value: TransportationFast) -> dict:
        return {"type": value.value}


class TimeMapFastArrivalSearches(BaseModel):
    """
    Attributes:
        many_to_one: Searches showing areas that can reach a destination (convergence)
        one_to_many: Searches showing areas reachable from an origin (divergence)
    """

    many_to_one: List[TimeMapFastSearch]
    one_to_many: List[TimeMapFastSearch]


class TimeMapFastRequest(TravelTimeRequest[TimeMapResponse]):
    """
    High-performance isochrone endpoint that creates travel time polygons showing
    reachable areas within specified travel times. Optimized for speed with
    limited configurability compared to the standard time-map endpoint.

    Attributes:
        arrival_searches: Isochrone search configurations for fast polygon generation
    """

    arrival_searches: TimeMapFastArrivalSearches

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        return [
            TimeMapFastRequest(
                arrival_searches=TimeMapFastArrivalSearches(
                    one_to_many=one_to_many, many_to_one=many_to_one
                ),
            )
            for one_to_many, many_to_one in split(
                self.arrival_searches.one_to_many,
                self.arrival_searches.many_to_one,
                window_size,
            )
        ]

    def merge(self, responses: List[TimeMapResponse]) -> TimeMapResponse:
        return TimeMapResponse(
            results=flatten([response.results for response in responses])
        )
