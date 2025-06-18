import typing
from datetime import datetime

from typing import List, Optional

from pydantic.main import BaseModel

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
    H3Centroid,
    Snapping,
    Range,
)
from traveltimepy.requests.request import TravelTimeRequest
from traveltimepy.responses.h3 import H3Response
from traveltimepy.itertools import split, flatten


class H3DepartureSearch(BaseModel):
    """
    Departure-based travel time search for H3 cells.

    Calculates reachable H3 cells from a departure location within specified travel time.

    Attributes:
        id: Unique identifier for this search
        coords: Departure location coordinates or H3 cell centroid
        departure_time: Specific departure time for the journey
        travel_time: Maximum journey time in seconds
        transportation: Transportation method (public_transport, driving, walking, etc.)
        range: Optional distance/time range constraints
        snapping: Optional road network lookup settings
    """

    id: str
    coords: typing.Union[Coordinates, H3Centroid]
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
    snapping: Optional[Snapping] = None


class H3ArrivalSearch(BaseModel):
    """
    Arrival-based travel time search for H3 cells.

    Calculates H3 cells that can reach an arrival location within specified travel time.

    Attributes:
        id: Unique identifier for this search
        coords: Arrival location coordinates or H3 cell centroid
        arrival_time: Specific arrival time for the journey
        travel_time: Maximum journey time in seconds
        transportation: Transportation method (public_transport, driving, walking, etc.)
        range: Optional distance/time range constraints
        snapping: Optional road network lookup settings
    """

    id: str
    coords: typing.Union[Coordinates, H3Centroid]
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
    snapping: Optional[Snapping] = None


class H3Intersection(BaseModel):
    """
    Defines intersection of multiple H3 search results.

    Creates a new shape containing only H3 cells that appear in ALL referenced searches.
    Useful for finding areas accessible from multiple locations or transport modes.

    Attributes:
        id: Unique identifier for this intersection
        search_ids: List of search IDs to intersect
    """

    id: str
    search_ids: List[str]


class H3Union(BaseModel):
    """
    Defines union of multiple H3 search results.

    Creates a new shape containing H3 cells that appear in ANY of the referenced searches.
    Useful for combining coverage areas from multiple searches.

    Attributes:
        id: Unique identifier for this union
        search_ids: List of search IDs to combine
    """

    id: str
    search_ids: List[str]


class H3Request(TravelTimeRequest[H3Response]):
    """
    Provides comprehensive H3 analysis with full configurability including specific
    departure/arrival times, unions, and intersections of search results.

    Attributes:
        resolution: H3 resolution level (1-9, higher = more granular cells)
        properties: Statistical properties to calculate for each H3 cell
        departure_searches: List of departure-based searches
        arrival_searches: List of arrival-based searches
        unions: List of union operations on search results
        intersections: List of intersection operations on search results
    """

    resolution: int
    properties: List[CellProperty]
    departure_searches: List[H3DepartureSearch]
    arrival_searches: List[H3ArrivalSearch]
    unions: List[H3Union]
    intersections: List[H3Intersection]

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        # Do not split request if unions/intersections are defined
        if len(self.unions) > 0 or len(self.intersections) > 0:
            return [self]
        else:
            chunks = split(self.departure_searches, self.arrival_searches, window_size)

            return [
                H3Request(
                    resolution=self.resolution,
                    properties=self.properties,
                    departure_searches=departures,
                    arrival_searches=arrivals,
                    unions=self.unions,
                    intersections=self.intersections,
                )
                for departures, arrivals in chunks
            ]

    def merge(self, responses: List[H3Response]) -> H3Response:
        return H3Response(
            results=sorted(
                flatten([response.results for response in responses]),
                key=lambda res: res.search_id,
            )
        )
