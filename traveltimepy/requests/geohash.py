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

    Attributes:
        id: Unique identifier for this search operation.
        coords: Departure location using either lat/lng coordinates or geohash centroid.
        departure_time: Leave departure location at no earlier than this time.
        travel_time: Maximum journey time in seconds. Maximum value is 14400 (4 hours).
        transportation: Transportation mode for the journey calculation.
        range: Optional departure time window for range search functionality.
        snapping: Configuration for connecting coordinates to the transportation network.
    """

    id: str
    coords: typing.Union[Coordinates, GeohashCentroid]
    departure_time: datetime
    travel_time: int = Field(le=14400)
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
    snapping: Optional[Snapping] = None


class GeoHashArrivalSearch(BaseModel):
    """
    Calculates travel times from all geohash cells to an arrival location within a travel time catchment area.

    Attributes:
        id: Unique identifier for this search operation.
        coords: Arrival location using either lat/lng coordinates or geohash centroid.
        arrival_time: Arrive at destination location at no later than this time.
        travel_time: Maximum journey time in seconds. Maximum value is 14400 (4 hours).
        transportation: Transportation mode for the journey calculation.
        range: Optional arrival time window for range search functionality.
        snapping: Configuration for connecting coordinates to the transportation network.
    """

    id: str
    coords: typing.Union[Coordinates, GeohashCentroid]
    arrival_time: datetime
    travel_time: int = Field(le=14400)
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
    snapping: Optional[Snapping] = None


class GeoHashIntersection(BaseModel):
    """
    Configuration for calculating intersection of geohash search results.

    Finds geohash cells that are reachable in ALL specified searches.

    Attributes:
        id: Unique identifier for this intersection operation.
        search_ids: List of search IDs to intersect. Must reference valid departure or arrival searches.
    """

    id: str
    search_ids: List[str]


class GeoHashUnion(BaseModel):
    """
    Configuration for calculating union of geohash search results.

    Combines geohash cells that are reachable in ANY of the specified searches.

    Attributes:
        id: Unique identifier for this union operation.
        search_ids: List of search IDs to combine. Must reference valid departure or arrival searches.
    """

    id: str
    search_ids: List[str]


class GeoHashRequest(TravelTimeRequest[GeoHashResponse]):
    """
    Request for geohash travel time analysis.

    Calculates travel times to geohash cells within travel time catchment areas,
    returning min, max, and mean travel times for each cell. More configurable
    than geohash-fast but with lower performance.

    Attributes:
        resolution: Geohash resolution of results. Valid range: 1-6.
        properties: Properties to return for each cell. Options: min, max, mean travel times.
        departure_searches: List of departure-based geohash searches.
        arrival_searches: List of arrival-based geohash searches.
        unions: List of union operations to perform on search results.
        intersections: List of intersection operations to perform on search results.
    """

    resolution: int
    properties: List[CellProperty]
    departure_searches: List[GeoHashDepartureSearch]
    arrival_searches: List[GeoHashArrivalSearch]
    unions: List[GeoHashUnion]
    intersections: List[GeoHashIntersection]

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
