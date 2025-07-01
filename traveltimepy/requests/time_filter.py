from datetime import datetime
from typing import List, Optional, Union

from pydantic.main import BaseModel

from traveltimepy.requests.common import Location, FullRange, Property, Snapping
from traveltimepy.requests.request import TravelTimeRequest
from traveltimepy.responses.time_filter import TimeFilterResponse
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


class TimeFilterArrivalSearch(BaseModel):
    """
    Calculates travel times from multiple departure locations to a single arrival
    location with specific arrival time and comprehensive transport options.

    Attributes:
        id: Unique identifier for this search
        departure_location_ids: List of departure location IDs
        arrival_location_id: Single arrival location ID
        arrival_time: Specific arrival time for the journey
        travel_time: Maximum journey time in seconds
        transportation: Transportation mode
        properties: Data to return (travel_time, distance, route, fares)
        range: Optional arrival time window for multiple journey options
        snapping: Optional road network lookup settings
    """

    id: str
    departure_location_ids: List[str]
    arrival_location_id: str
    arrival_time: datetime
    travel_time: int
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
    snapping: Optional[Snapping] = None


class TimeFilterDepartureSearch(BaseModel):
    """
    Calculates travel times from a single departure location to multiple arrival
    locations with specific departure time and comprehensive transport options.

    Attributes:
        id: Unique identifier for this search
        arrival_location_ids: List of arrival location IDs
        departure_location_id: Single departure location ID
        departure_time: Specific departure time for the journey
        travel_time: Maximum journey time in seconds
        transportation: Full range of transportation methods available
        properties: Data to return (travel_time, distance, route, fares)
        range: Optional departure time window for multiple journey options
        snapping: Optional road network lookup settings
    """

    id: str
    arrival_location_ids: List[str]
    departure_location_id: str
    departure_time: datetime
    travel_time: int
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
    snapping: Optional[Snapping] = None


class TimeFilterRequest(TravelTimeRequest[TimeFilterResponse]):
    """
    Full-featured distance matrix endpoint with comprehensive configurability
    including specific departure/arrival times, range searches, and all transport modes.

    Attributes:
        locations: List of all locations referenced by ID in searches
        departure_searches: List of departure-based searches (max 10)
        arrival_searches: List of arrival-based searches (max 10)
    """

    locations: List[Location]
    departure_searches: List[TimeFilterDepartureSearch]
    arrival_searches: List[TimeFilterArrivalSearch]

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        return [
            TimeFilterRequest(
                locations=self.locations,
                departure_searches=departures,
                arrival_searches=arrivals,
            )
            for departures, arrivals in split(
                self.departure_searches, self.arrival_searches, window_size
            )
        ]

    def merge(self, responses: List[TimeFilterResponse]) -> TimeFilterResponse:
        return TimeFilterResponse(
            results=flatten([response.results for response in responses])
        )
