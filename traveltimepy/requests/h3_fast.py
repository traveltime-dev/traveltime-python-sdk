from typing import List, Optional
import typing

from pydantic import BaseModel, field_serializer

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
from traveltimepy.requests.transportation import TransportationFast


class H3FastSearch(BaseModel):
    """
    Represents a single travel time search configuration for the H3 Fast API.

    Attributes:
        id: Unique identifier for this search - must be unique across all searches in a request
        coords: Starting/ending coordinates - can be lat/lng coordinates or H3 cell centroid
        transportation: Transportation method (public_transport, walking+ferry, cycling+ferry, etc.)
        travel_time: Maximum journey time in seconds (max 10800s)
        arrival_time_period: Time period for the search
        snapping: Optional settings for adjusting road network lookup behavior
    """

    id: str
    coords: typing.Union[Coordinates, H3Centroid]
    transportation: TransportationFast
    travel_time: int
    arrival_time_period: ArrivalTimePeriod = ArrivalTimePeriod.WEEKDAY_MORNING
    snapping: Optional[Snapping] = None

    # JSON expects `"transportation": { "type": "public_transport" }` and not `"transportation": "public_transport"`
    @field_serializer("transportation")
    def serialize_transportation(self, value: TransportationFast) -> dict:
        return {"type": value.value}


class H3FastArrivalSearches(BaseModel):
    """
    The H3 Fast API supports two main search patterns for calculating travel time catchments.

    Attributes:
        many_to_one: Searches that calculate travel times from multiple origins to one destination.
        one_to_many: Searches that calculate travel times from one origin to multiple destinations.
    """

    many_to_one: List[H3FastSearch]
    one_to_many: List[H3FastSearch]


class H3FastRequest(TravelTimeRequest[H3Response]):
    """
    Request calculates travel times to all H3 hexagonal cells within a travel time
    catchment area and returns min/max/mean travel times for each cell.

    H3 is hexagonal hierarchical spatial indexing system that divides
    the Earth's surface into hexagonal cells at different resolutions.

    Attributes:
        resolution: H3 resolution level for results (1-9, where higher = more granular/smaller cells).
        properties: Properties to return for each H3 cell (min, max, mean travel times).
        arrival_searches: Arrival-based search configurations containing the actual search
                         definitions that will be executed.
    """

    resolution: int
    properties: List[CellProperty]
    arrival_searches: H3FastArrivalSearches

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        return [
            H3FastRequest(
                resolution=self.resolution,
                properties=self.properties,
                arrival_searches=H3FastArrivalSearches(
                    one_to_many=one_to_many, many_to_one=many_to_one
                ),
            )
            for one_to_many, many_to_one in split(
                self.arrival_searches.one_to_many,
                self.arrival_searches.many_to_one,
                window_size,
            )
        ]

    def merge(self, responses: List[H3Response]) -> H3Response:
        return H3Response(results=flatten([response.results for response in responses]))
