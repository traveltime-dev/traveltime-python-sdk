from typing import List, Optional, Union

from pydantic import BaseModel

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
from traveltimepy.requests.transportation import (
    PublicTransportFast,
    DrivingFast,
    CyclingFast,
    WalkingFast,
    WalkingFerryFast,
    CyclingFerryFast,
    DrivingFerryFast,
    DrivingPublicTransportFast,
)


class TimeMapFastSearch(BaseModel):
    """Creates travel time catchment areas (isochrones) showing all locations reachable
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
        buffer_distance: Optional integer. minimum value is 250 meters. Default value is 1000 meters.
                - When `render_mode=approximate_time_filter` - controls how far from the reached road
                  network the isochrone generation algorithm may consider locations as reachable.
                - When `render_mode=road_buffering` - controls how far the final polygon is expanded
                  outward from the reached roads. This behaves like applying a positive geometric offset
                  to the collection of lines derived from the reached road segments.
    """

    id: str
    coords: Coordinates
    transportation: Union[
        PublicTransportFast,
        DrivingFast,
        CyclingFast,
        WalkingFast,
        WalkingFerryFast,
        CyclingFerryFast,
        DrivingFerryFast,
        DrivingPublicTransportFast,
    ]
    travel_time: int
    arrival_time_period: ArrivalTimePeriod = ArrivalTimePeriod.WEEKDAY_MORNING
    level_of_detail: Optional[LevelOfDetail] = None
    snapping: Optional[Snapping] = None
    polygons_filter: Optional[PolygonsFilter] = None
    render_mode: Optional[RenderMode] = None
    buffer_distance: Optional[int] = None


class TimeMapFastArrivalSearches(BaseModel):
    """
    Attributes:
        many_to_one: Searches showing areas that can reach a destination (convergence)
        one_to_many: Searches showing areas reachable from an origin (divergence)
    """

    many_to_one: List[TimeMapFastSearch]
    one_to_many: List[TimeMapFastSearch]


class TimeMapFastIntersection(BaseModel):
    """Defines intersection of multiple Time Map Fast search results.

    Creates a new shape containing only the area that appears in ALL referenced searches.
    Useful for finding areas accessible from multiple locations or transport modes.

    Attributes:
        id: Unique identifier for this intersection
        search_ids: List of search IDs to intersect
    """

    id: str
    search_ids: List[str]


class TimeMapFastUnion(BaseModel):
    """Defines union of multiple Time Map Fast search results.

    Creates a new shape containing the area that appears in ANY of the referenced searches.
    Useful for combining coverage areas from multiple searches.

    Attributes:
        id: Unique identifier for this union
        search_ids: List of search IDs to combine
    """

    id: str
    search_ids: List[str]


class TimeMapFastRequest(TravelTimeRequest[TimeMapResponse]):
    """High-performance isochrone endpoint that creates travel time polygons showing
    reachable areas within specified travel times. Optimized for speed with limited
    configurability compared to the standard time-map endpoint.

    Attributes:
        arrival_searches: Isochrone search configurations for fast polygon generation
        unions: List of union operations on search results
        intersections: List of intersection operations on search results
    """

    arrival_searches: TimeMapFastArrivalSearches
    unions: Optional[List[TimeMapFastUnion]]
    intersections: Optional[List[TimeMapFastIntersection]]

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        # Do not split request if unions/intersections are defined
        if self.unions or self.intersections:
            return [self]
        else:
            return [
                TimeMapFastRequest(
                    arrival_searches=TimeMapFastArrivalSearches(
                        one_to_many=one_to_many, many_to_one=many_to_one
                    ),
                    unions=self.unions,
                    intersections=self.intersections,
                )
                for one_to_many, many_to_one in split(
                    self.arrival_searches.one_to_many,
                    self.arrival_searches.many_to_one,
                    window_size,
                )
            ]

    def merge(self, responses: List[TimeMapResponse]) -> TimeMapResponse:
        return TimeMapResponse(
            results=sorted(
                flatten([response.results for response in responses]),
                key=lambda res: res.search_id,
            )
        )
