from datetime import datetime
from typing import List, Union, Optional

from pydantic import BaseModel

from traveltimepy.requests.common import Coordinates, Property, FullRange
from traveltimepy.requests.request import TravelTimeRequest
from traveltimepy.responses.postcodes import PostcodesResponse
from traveltimepy.itertools import split, flatten
from traveltimepy.requests.transportation import (
    PublicTransport,
    Driving,
    Ferry,
    Walking,
    Cycling,
    DrivingTrain,
    CyclingPublicTransport,
)


class PostcodeArrivalSearch(BaseModel):
    """
    Arrival-based postcode search configuration.

    Finds postcodes that can reach an arrival location within specified travel time.

    Attributes:
        id: Unique identifier for this search
        coords: Arrival location coordinates (lat/lng)
        travel_time: Maximum journey time in seconds (max 14,400 = 4 hours)
        arrival_time: Specific arrival time
        transportation: Transportation method (driving, public_transport, walking, etc.)
        properties: Data to return for each postcode (travel_time, distance)
        range: Optional arrival time window for multiple journey options
    """

    id: str
    coords: Coordinates
    travel_time: int
    arrival_time: datetime
    transportation: Union[
        PublicTransport,
        Driving,
        Ferry,
        Walking,
        Cycling,
        DrivingTrain,
        CyclingPublicTransport,
    ]
    properties: List[Property]
    range: Optional[FullRange] = None


class PostcodeDepartureSearch(BaseModel):
    """
    Departure-based postcode search configuration.

    Finds reachable postcodes from a departure location within specified travel time.

    Attributes:
        id: Unique identifier for this search
        coords: Departure location coordinates (lat/lng)
        travel_time: Maximum journey time in seconds (max 14,400 = 4 hours)
        departure_time: Specific departure time
        transportation: Transportation method (driving, public_transport, walking, etc.)
        properties: Data to return for each postcode (travel_time, distance)
        range: Optional departure time window for multiple journey options
    """

    id: str
    coords: Coordinates
    travel_time: int
    departure_time: datetime
    transportation: Union[
        PublicTransport,
        Driving,
        Ferry,
        Walking,
        Cycling,
        DrivingTrain,
        CyclingPublicTransport,
    ]
    properties: List[Property]
    range: Optional[FullRange] = None


class PostcodesRequest(TravelTimeRequest[PostcodesResponse]):
    """
    Finds reachable postcodes and returns travel statistics.

    Attributes:
        departure_searches: List of departure-based postcode searches (max 10)
        arrival_searches: List of arrival-based postcode searches (max 10)
    """

    departure_searches: List[PostcodeDepartureSearch]
    arrival_searches: List[PostcodeArrivalSearch]

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        return [
            PostcodesRequest(departure_searches=departures, arrival_searches=arrivals)
            for departures, arrivals in split(
                self.departure_searches, self.arrival_searches, window_size
            )
        ]

    def merge(self, responses: List[PostcodesResponse]) -> PostcodesResponse:
        return PostcodesResponse(
            results=sorted(
                flatten([response.results for response in responses]),
                key=lambda res: res.search_id,
            )
        )
