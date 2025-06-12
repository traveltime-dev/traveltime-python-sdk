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

    Example:
        Generate a map showing all areas within 5km walking distance from a city center:

        search = DistanceMapDepartureSearch(
            id="city_center_walk",
            coords=Coordinates(lat=51.5074, lng=-0.1278),  # London
            departure_time=datetime.now(),
            travel_distance=5000,  # 5km in meters
            transportation=Walking()
        )

    """

    id: str
    """
    Unique identifier for this distance map search.
    Used to reference and track the search request.
    """

    coords: Coordinates
    """
    Starting location for the distance map calculation.
    All reachable areas will be calculated from this departure point.
    """

    departure_time: datetime
    """
    Time of departure for the journey calculation.
    """

    travel_distance: int
    """
    Maximum travel distance in meters from the departure location.
    Defines the boundary of the reachable area - no point in the resulting polygon
    will require more than this distance to reach from the departure coordinates.
    """

    transportation: typing.Union[
        PublicTransport,
        Driving,
        Ferry,
        Walking,
        Cycling,
        DrivingTrain,
        CyclingPublicTransport,
    ]
    """
    Transportation mode to use for calculating reachable areas.
    """

    level_of_detail: Optional[LevelOfDetail] = None
    """
    Controls the precision and complexity of the returned polygon geometry.
    Higher detail provides more accurate boundaries but increases computation time and response size.
    """

    snapping: Optional[Snapping] = None
    """
    Configuration for connecting the departure coordinates to the transportation network.
    Determines how off-road distances are handled and which road types are acceptable connection points.
    """

    polygons_filter: Optional[PolygonsFilter] = None
    """
    Limits the number of polygons returned in the result.
    Useful when the reachable area consists of multiple disconnected regions
    and you only want the largest or most significant areas.
    """

    no_holes: Optional[bool] = None
    """
    Enable to remove holes from returned polygons.
    Note that this will likely result in loss in accuracy.
    """


class DistanceMapArrivalSearch(BaseModel):
    """
    Configuration for generating a reverse distance map (isodistance polygon) to an arrival location.

    A reverse distance map shows all areas from which you can reach a destination within a specified
    travel distance, arriving by a certain time using the specified transportation method. This is
    the inverse of a departure search - instead of "where can I go from here?", it answers
    "where can I come from to get here?".

    Example:
        Generate a map showing all areas within 3km cycling distance that can reach
        a train station by 8:00 AM:

        search = DistanceMapArrivalSearch(
            id="station_catchment",
            coords=Coordinates(lat=51.5074, lng=-0.1278),  # Train station
            arrival_time=datetime(2024, 1, 15, 8, 0),  # 8:00 AM
            travel_distance=3000,  # 3km in meters
            transportation=Cycling()
        )
    """

    id: str
    """
    Unique identifier for this distance map search.
    Used to reference and track the search request.
    """

    coords: Coordinates
    """
    Destination location for the distance map calculation.
    All origin areas will be calculated based on their ability to reach this arrival point.
    """

    arrival_time: datetime
    """
    Required arrival time at the destination.
    The search finds areas that can reach the destination by this time.
    """

    travel_distance: int
    """
    Maximum travel distance in meters to the arrival location.
    Defines the boundary of the origin area - no point in the resulting polygon
    will require more than this distance to reach the arrival coordinates.
    """

    transportation: typing.Union[
        PublicTransport,
        Driving,
        Ferry,
        Walking,
        Cycling,
        DrivingTrain,
        CyclingPublicTransport,
    ]
    """
    Transportation mode to use for calculating origin areas.
    """

    level_of_detail: Optional[LevelOfDetail] = None
    """
    Controls the precision and complexity of the returned polygon geometry.
    Higher detail provides more accurate boundaries but increases computation time and response size.
    """

    snapping: Optional[Snapping] = None
    """
    Configuration for connecting the arrival coordinates to the transportation network.
    Determines how off-road distances are handled and which road types are acceptable connection points.
    """

    polygons_filter: Optional[PolygonsFilter] = None
    """
    Limits the number of polygons returned in the result.
    Useful when the reachable area consists of multiple disconnected regions
    and you only want the largest or most significant areas.
    """

    no_holes: Optional[bool] = None
    """
    Enable to remove holes from returned polygons.
    Note that this will likely result in loss in accuracy.
    """


class DistanceMapIntersection(BaseModel):
    """
    Configuration for calculating the intersection of multiple distance map searches.

    An intersection operation finds areas that are reachable by ALL specified searches.
    This is useful for finding locations that satisfy multiple accessibility criteria simultaneously,
    such as areas within walking distance of both a train station and a shopping center.

    Example:
        Find areas within walking distance of both a train station and a hospital:

        intersection = DistanceMapIntersection(
            id="station_and_hospital",
            search_ids=["train_station_walk", "hospital_walk"]
        )

        The result will only include areas that appear in both individual distance maps.
    """

    id: str
    """
    Unique identifier for this intersection operation.
    Used to reference the intersection result in the response.
    """

    search_ids: List[str]
    """
    List of distance map search IDs to intersect.
    Must reference valid departure or arrival search IDs within the same request.
    The intersection will only include areas that are reachable in ALL referenced searches.
    Requires at least 2 search IDs to perform a meaningful intersection.
    """


class DistanceMapUnion(BaseModel):
    """
    Configuration for calculating the union of multiple distance map searches.

    A union operation combines all areas that are reachable by ANY of the specified searches.
    This is useful for finding the total coverage area of multiple access points or transportation
    options, such as the combined catchment area of several bus stops or train stations.

    Example:
        Find the combined area within cycling distance of three bike share stations:

        union = DistanceMapUnion(
            id="bike_share_coverage",
            search_ids=["station_a_cycle", "station_b_cycle", "station_c_cycle"]
        )

        The result will include all areas that appear in any of the individual distance maps.
    """

    id: str
    """
    Unique identifier for this union operation.
    Used to reference the union result in the response.
    """

    search_ids: List[str]
    """
    List of distance map search IDs to combine.
    Must reference valid departure or arrival search IDs within the same request.
    The union will include areas that are reachable in ANY of the referenced searches.
    Requires at least 2 search IDs to perform a meaningful union.
    """


class DistanceMapRequest(TravelTimeRequest[TimeMapResponse]):

    departure_searches: List[DistanceMapDepartureSearch]
    """
    List of departure-based distance map searches.
    Each search calculates areas reachable FROM a specific starting point.
    """

    arrival_searches: List[DistanceMapArrivalSearch]
    """
    List of arrival-based distance map searches.
    Each search calculates areas that can reach TO a specific destination.
    """

    unions: List[DistanceMapUnion]
    """
    List of union operations to perform on the search results.
    Each union combines multiple searches to show total coverage area.
    Search IDs must reference searches defined in departure_searches or arrival_searches.
    """

    intersections: List[DistanceMapIntersection]
    """
    List of intersection operations to perform on the search results.
    Each intersection finds overlapping areas between multiple searches.
    Search IDs must reference searches defined in departure_searches or arrival_searches.
    """

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
