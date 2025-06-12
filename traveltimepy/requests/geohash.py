import typing
from datetime import datetime
from typing import List, Optional

from pydantic import Field
from pydantic.main import BaseModel

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
from traveltimepy.requests.common import (
    CellProperty,
    Coordinates,
    GeohashCentroid,
    Snapping,
    Range,
)
from traveltimepy.itertools import split, flatten
from traveltimepy.responses.geohash import GeoHashResponse


class GeoHashDepartureSearch(BaseModel):
    """
    Calculates travel times from a departure location to all geohash cells within a travel time catchment area.
    """

    id: str
    """Unique identifier for this search operation."""

    coords: typing.Union[Coordinates, GeohashCentroid]
    """Departure location using either lat/lng coordinates or geohash centroid."""

    departure_time: datetime
    """Leave departure location at no earlier than this time."""

    travel_time: int
    """Maximum journey time in seconds. Maximum value is 14400 (4 hours)."""

    transportation: typing.Union[
        PublicTransport,
        Driving,
        Ferry,
        Walking,
        Cycling,
        DrivingTrain,
        CyclingPublicTransport,
    ]
    """Transportation mode for the journey calculation."""

    range: Optional[Range] = None
    """Optional departure time window for range search functionality."""

    snapping: Optional[Snapping] = None
    """Configuration for connecting coordinates to the transportation network."""


class GeoHashArrivalSearch(BaseModel):
    """
    Calculates travel times from all geohash cells to an arrival location within a travel time catchment area.
    """

    id: str
    """Unique identifier for this search operation."""

    coords: typing.Union[Coordinates, GeohashCentroid]
    """Arrival location using either lat/lng coordinates or geohash centroid."""

    arrival_time: datetime
    """Arrive at destination location at no later than this time."""

    travel_time: int = Field(le=14400)
    """Maximum journey time in seconds. Maximum value is 14400 (4 hours)."""

    transportation: typing.Union[
        PublicTransport,
        Driving,
        Ferry,
        Walking,
        Cycling,
        DrivingTrain,
        CyclingPublicTransport,
    ]
    """Transportation mode for the journey calculation."""

    range: Optional[Range] = None
    """Optional arrival time window for range search functionality."""

    snapping: Optional[Snapping] = None
    """Configuration for connecting coordinates to the transportation network."""


class GeoHashIntersection(BaseModel):
    """
    Configuration for calculating intersection of geohash search results.

    Finds geohash cells that are reachable in ALL specified searches.
    """

    id: str
    """Unique identifier for this intersection operation."""

    search_ids: List[str]
    """List of search IDs to intersect. Must reference valid departure or arrival searches."""


class GeoHashUnion(BaseModel):
    """
    Configuration for calculating union of geohash search results.

    Combines geohash cells that are reachable in ANY of the specified searches.
    """

    id: str
    """Unique identifier for this union operation."""

    search_ids: List[str]
    """List of search IDs to combine. Must reference valid departure or arrival searches."""


class GeoHashRequest(TravelTimeRequest[GeoHashResponse]):
    """
    Request for geohash travel time analysis.

    Calculates travel times to geohash cells within travel time catchment areas,
    returning min, max, and mean travel times for each cell. More configurable
    than geohash-fast but with lower performance.
    """

    resolution: int
    """Geohash resolution of results. Valid range: 1-6."""

    properties: List[CellProperty]
    """Properties to return for each cell. Options: min, max, mean travel times."""

    departure_searches: List[GeoHashDepartureSearch]
    """List of departure-based geohash searches."""

    arrival_searches: List[GeoHashArrivalSearch]
    """List of arrival-based geohash searches."""

    unions: List[GeoHashUnion]
    """List of union operations to perform on search results."""

    intersections: List[GeoHashIntersection]
    """List of intersection operations to perform on search results."""

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        # Do not split request if unions/intersections are defined
        if len(self.unions) > 0 or len(self.intersections) > 0:
            return [self]
        else:
            chunks = split(self.departure_searches, self.arrival_searches, window_size)

            return [
                GeoHashRequest(
                    resolution=self.resolution,
                    properties=self.properties,
                    departure_searches=departures,
                    arrival_searches=arrivals,
                    unions=self.unions,
                    intersections=self.intersections,
                )
                for departures, arrivals in chunks
            ]

    def merge(self, responses: List[GeoHashResponse]) -> GeoHashResponse:
        return GeoHashResponse(
            results=sorted(
                flatten([response.results for response in responses]),
                key=lambda res: res.search_id,
            )
        )
