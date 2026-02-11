from typing import List, Optional
import typing

from pydantic import BaseModel

from traveltimepy.requests.common import (
    CellProperty,
    Coordinates,
    H3Centroid,
    Snapping,
    ArrivalTimePeriod,
)
from traveltimepy.requests.request import TravelTimeRequest
from traveltimepy.responses.h3 import H3Response
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


class H3FastSearch(BaseModel):
    """Represents a single travel time search configuration for the H3 Fast API.

    Attributes:
        id: Unique identifier for this search - must be unique across all searches in a request
        coords: Starting/ending coordinates - can be lat/lng coordinates or H3 cell centroid
        transportation: Transportation method (use DrivingFast or DrivingFerryFast for traffic_model)
        travel_time: Maximum journey time in seconds (max 10800s).
                         Maximum value depends on resolution parameter.
                         Limitations can be found here:
                         https://docs.traveltime.com/api/reference/h3-fast#limits-of-resolution-and-traveltime.
        arrival_time_period: Time period for the search
        snapping: Optional settings for adjusting road network lookup behavior
    """

    id: str
    coords: typing.Union[Coordinates, H3Centroid]
    transportation: typing.Union[
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
    snapping: Optional[Snapping] = None


class H3FastArrivalSearches(BaseModel):
    """The H3 Fast API supports two main search patterns for calculating travel time
    catchments.

    Attributes:
        many_to_one: Searches that calculate travel times from multiple origins to one destination.
        one_to_many: Searches that calculate travel times from one origin to multiple destinations.
    """

    many_to_one: List[H3FastSearch]
    one_to_many: List[H3FastSearch]


class H3FastIntersection(BaseModel):
    """Defines intersection of multiple H3 Fast search results.

    Creates a new shape containing only H3 cells that appear in ALL referenced searches.
    Useful for finding areas accessible from multiple locations or transport modes.

    Attributes:
        id: Unique identifier for this intersection
        search_ids: List of search IDs to intersect
    """

    id: str
    search_ids: List[str]


class H3FastUnion(BaseModel):
    """Defines union of multiple H3 Fast search results.

    Creates a new shape containing H3 cells that appear in ANY of the referenced searches.
    Useful for combining coverage areas from multiple searches.

    Attributes:
        id: Unique identifier for this union
        search_ids: List of search IDs to combine
    """

    id: str
    search_ids: List[str]


class H3FastRequest(TravelTimeRequest[H3Response]):
    """Request calculates travel times to all H3 hexagonal cells within a travel time
    catchment area and returns min/max/mean travel times for each cell.

    H3 is hexagonal hierarchical spatial indexing system that divides
    the Earth's surface into hexagonal cells at different resolutions.

    Attributes:
        resolution: H3 resolution level (higher = more granular cells).
                         Limitations can be found here:
                         https://docs.traveltime.com/api/reference/h3-fast#limits-of-resolution-and-traveltime.
        properties: Properties to return for each H3 cell (min, max, mean travel times).
        arrival_searches: Arrival-based search configurations containing the actual search
                         definitions that will be executed.
        unions: List of union operations on search results
        intersections: List of intersection operations on search results
    """

    resolution: int
    properties: List[CellProperty]
    arrival_searches: H3FastArrivalSearches
    unions: List[H3FastUnion]
    intersections: List[H3FastIntersection]

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        # Do not split request if unions/intersections are defined
        if len(self.unions) > 0 or len(self.intersections) > 0:
            return [self]
        else:
            return [
                H3FastRequest(
                    resolution=self.resolution,
                    properties=self.properties,
                    arrival_searches=H3FastArrivalSearches(
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

    def merge(self, responses: List[H3Response]) -> H3Response:
        return H3Response(
            results=sorted(
                flatten([response.results for response in responses]),
                key=lambda res: res.search_id,
            )
        )
