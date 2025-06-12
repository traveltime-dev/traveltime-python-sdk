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
    """

    id: str
    """Unique identifier for this search operation."""

    coords: typing.Union[Coordinates, GeohashCentroid]
    """Location coordinates using either lat/lng or geohash centroid."""

    transportation: TransportationFast
    """Transportation mode for the journey calculation."""

    travel_time: int
    """Maximum journey time in seconds. Maximum value is 10800 (3 hours)."""

    arrival_time_period: ArrivalTimePeriod = ArrivalTimePeriod.WEEKDAY_MORNING
    """Time period for the search"""

    snapping: Optional[Snapping] = None
    """Configuration for connecting coordinates to the transportation network."""

    @field_serializer("transportation")
    def serialize_transportation(self, value: TransportationFast) -> dict:
        return {"type": value.value}


class GeoHashFastArrivalSearches(BaseModel):

    many_to_one: List[GeoHashFastSearch]
    """Searches from multiple departure locations to one arrival location."""

    one_to_many: List[GeoHashFastSearch]
    """Searches from one departure location to multiple arrival locations."""


class GeoHashFastRequest(TravelTimeRequest[GeoHashResponse]):
    """
    High-performance version with limited parameters and geographic coverage.
    """

    resolution: int
    """Geohash resolution of results. Valid range: 1-6."""

    properties: List[CellProperty]
    """Properties to return for each cell. Options: min, max, mean travel times."""

    arrival_searches: GeoHashFastArrivalSearches
    """Arrival-based searches"""

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
