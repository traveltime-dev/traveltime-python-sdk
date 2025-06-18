import typing
from datetime import datetime

from typing import List, Optional

from pydantic.main import BaseModel

from traveltimepy.requests.common import Snapping, PolygonsFilter
from traveltimepy.requests.level_of_detail import LevelOfDetail
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
from traveltimepy.itertools import split, flatten
from traveltimepy.requests.common import Coordinates
from traveltimepy.responses.time_map import TimeMapResponse


class DistanceMapDepartureSearch(BaseModel):
    """
    Configuration for generating a distance map (isodistance polygon) from a departure location.

    A distance map shows all areas reachable within a specified travel distance from a starting point,
    using the specified transportation method and departure time. The result is typically a polygon
    or set of polygons representing the reachable area.

    Attributes:
        id: Unique identifier for this distance map search. Used to reference and track the search request.
        coords: Starting location for the distance map calculation.
                All reachable areas will be calculated from this departure point.
        departure_time: Time of departure for the journey calculation.
        travel_distance: Maximum travel distance in meters from the departure location.
                         Defines the boundary of the reachable area.
        transportation: Transportation mode to use for calculating reachable areas.
        level_of_detail: Controls the precision and complexity of the returned polygon geometry.
                         Higher detail provides more accurate boundaries.
        snapping: Configuration for connecting the departure coordinates to the transportation network.
        polygons_filter: Limits the number of polygons returned in the result.
                         Useful when the reachable area consists of multiple disconnected regions.
        no_holes: Enable to remove holes from returned polygons. Note that this will likely result in loss in accuracy.
    """

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
    """
    Configuration for generating a reverse distance map (isodistance polygon) to an arrival location.

    A reverse distance map shows all areas from which you can reach a destination within a specified
    travel distance, arriving by a certain time using the specified transportation method. This is
    the inverse of a departure search - instead of "where can I go from here?", it answers
    "where can I come from to get here?".

    Attributes:
        id: Unique identifier for this distance map search. Used to reference and track the search request.
        coords: Destination location for the distance map calculation.
                All origin areas will be calculated based on their ability to reach this arrival point.
        arrival_time: Required arrival time at the destination.
                      The search finds areas that can reach the destination by this time.
        travel_distance: Maximum travel distance in meters to the arrival location.
                         Defines the boundary of the origin area.
        transportation: Transportation mode to use for calculating origin areas.
        level_of_detail: Controls the precision and complexity of the returned polygon geometry.
                         Higher detail provides more accurate boundaries.
        snapping: Configuration for connecting the arrival coordinates to the transportation network.
        polygons_filter: Limits the number of polygons returned in the result.
                         Useful when the reachable area consists of multiple disconnected regions.
        no_holes: Enable to remove holes from returned polygons. Note that this will likely result in loss in accuracy.
    """

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
    """
    An intersection operation finds areas that are reachable by ALL specified searches.
    This is useful for finding locations that satisfy multiple accessibility criteria simultaneously,
    such as areas within walking distance of both a train station and a shopping center.

    Attributes:
        id: Unique identifier for this intersection operation.
            Used to reference the intersection result in the response.
        search_ids: List of distance map search IDs to intersect.
                    Must reference valid departure or arrival search IDs within the same request.
                    The intersection will only include areas that are reachable in ALL referenced searches.
                    Requires at least 2 search IDs.
    """

    id: str
    search_ids: List[str]


class DistanceMapUnion(BaseModel):
    """
    A union operation combines all areas that are reachable by ANY of the specified searches.
    This is useful for finding the total coverage area of multiple access points or transportation
    options, such as the combined catchment area of several bus stops or train stations.

    Attributes:
        id: Unique identifier for this union operation. Used to reference the union result in the response.
        search_ids: List of distance map search IDs to combine.
                    Must reference valid departure or arrival search IDs within the same request.
                    The union will include areas that are reachable in ANY of the referenced searches.
                    Requires at least 2 search IDs.
    """

    id: str
    search_ids: List[str]


class DistanceMapRequest(TravelTimeRequest[TimeMapResponse]):
    """
    Generates isodistance polygons showing areas reachable within specified travel distances
    rather than travel times. Supports departure/arrival searches, unions, and intersections.

    Attributes:
        departure_searches: List of departure-based distance map searches.
                            Each search calculates areas reachable FROM a specific starting point.
        arrival_searches: List of arrival-based distance map searches.
                          Each search calculates areas that can reach TO a specific destination.
        unions: List of union operations to perform on the search results.
                Each union combines multiple searches to show total coverage area.
        intersections: List of intersection operations to perform on the search results.
                       Each intersection finds overlapping areas between multiple searches.
    """

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
