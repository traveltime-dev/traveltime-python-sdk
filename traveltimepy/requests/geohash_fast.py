from typing import List, Optional
import typing

from pydantic import BaseModel, field_serializer

from traveltimepy.requests.transportation import TransportationFast
from traveltimepy.requests.common import (
    CellProperty,
    Coordinates,
    GeohashCentroid,
    Snapping,
    ArrivalTimePeriod,
)
from traveltimepy.requests.request import TravelTimeRequest
from traveltimepy.responses.geohash import GeoHashResponse
from traveltimepy.itertools import split, flatten


class GeoHashFastSearch(BaseModel):
    """
    High-performance search that calculates travel times to geohash cells within a travel time catchment area.

    Optimized for speed with limited configurability compared to the standard geohash endpoint.
    Uses time periods instead of specific departure/arrival times for better performance.

    Attributes:
        id: Unique identifier for this search operation.
        coords: Location coordinates using either lat/lng or geohash centroid.
        transportation: Transportation mode for the journey calculation (limited options for performance).
        travel_time: Maximum journey time in seconds. Maximum value is 10800 (3 hours).
        arrival_time_period: Time period for the search instead of specific time.
        snapping: Configuration for connecting coordinates to the transportation network.
    """

    id: str
    coords: typing.Union[Coordinates, GeohashCentroid]
    transportation: TransportationFast
    travel_time: int
    arrival_time_period: ArrivalTimePeriod = ArrivalTimePeriod.WEEKDAY_MORNING
    snapping: Optional[Snapping] = None

    @field_serializer("transportation")
    def serialize_transportation(self, value: TransportationFast) -> dict:
        return {"type": value.value}


class GeoHashFastArrivalSearches(BaseModel):
    """
    Container for high-performance geohash arrival search patterns.

    Groups different search configurations for the Geohash Fast API to calculate
    travel times to geohash cells with optimized performance.

    Attributes:
        many_to_one: Searches from multiple departure locations to one arrival location.
        one_to_many: Searches from one departure location to multiple arrival locations.
    """

    many_to_one: List[GeoHashFastSearch]
    one_to_many: List[GeoHashFastSearch]


class GeoHashFastRequest(TravelTimeRequest[GeoHashResponse]):
    """
    High-performance geohash travel time analysis with limited parameters and geographic coverage.

    Optimized version of the geohash endpoint that trades configurability for speed and performance.
    Uses time periods instead of specific times and supports fewer transportation options.

    Attributes:
        resolution: Geohash resolution of results. Valid range: 1-6.
        properties: Properties to return for each cell. Options: min, max, mean travel times.
        arrival_searches: Arrival-based search configurations for fast geohash processing.

    Note:
        - High performance: optimized for speed over configurability
        - Limited transport options and time periods for performance
        - Max travel time: 10,800 seconds (3 hours)
        - Limited geographic coverage compared to standard geohash endpoint
    """

    resolution: int
    properties: List[CellProperty]
    arrival_searches: GeoHashFastArrivalSearches

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        return [
            GeoHashFastRequest(
                resolution=self.resolution,
                properties=self.properties,
                arrival_searches=GeoHashFastArrivalSearches(
                    one_to_many=one_to_many, many_to_one=many_to_one
                ),
            )
            for one_to_many, many_to_one in split(
                self.arrival_searches.one_to_many,
                self.arrival_searches.many_to_one,
                window_size,
            )
        ]

    def merge(self, responses: List[GeoHashResponse]) -> GeoHashResponse:
        return GeoHashResponse(
            results=flatten([response.results for response in responses])
        )
