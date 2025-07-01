from datetime import datetime
from typing import List, Optional, Union

from pydantic.main import BaseModel

from traveltimepy.requests.common import Location, Property, FullRange, Snapping
from traveltimepy.requests.transportation import (
    PublicTransport,
    Driving,
    Ferry,
    Walking,
    Cycling,
    DrivingTrain,
    CyclingPublicTransport,
)
from traveltimepy.requests.request import TravelTimeRequest
from traveltimepy.responses.routes import RoutesResponse
from traveltimepy.itertools import split, flatten


class RoutesArrivalSearch(BaseModel):
    """
    Arrival-based route search for A to B routing with turn-by-turn directions.

    Calculates routes from multiple departure locations to a single arrival location,
    returning detailed routing information including turn-by-turn directions.

    Attributes:
        id: Unique identifier for this search
        departure_location_ids: List of departure location IDs
        arrival_location_id: Single arrival location ID
        arrival_time: Specific arrival time for the journey
        transportation: Transportation method (driving, public_transport, walking, etc.)
        properties: Data to return (route, travel_time, distance, fares)
        range: Optional arrival time window for multiple journey options
        snapping: Optional road network lookup settings
    """

    id: str
    departure_location_ids: List[str]
    arrival_location_id: str
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
    snapping: Optional[Snapping] = None


class RoutesDepartureSearch(BaseModel):
    """
    Departure-based route search for A to B routing with turn-by-turn directions.

    Calculates routes from a single departure location to multiple arrival locations,
    returning detailed routing information including turn-by-turn directions.

    Attributes:
        id: Unique identifier for this search
        arrival_location_ids: List of arrival location IDs
        departure_location_id: Single departure location ID
        departure_time: Specific departure time for the journey
        transportation: Transportation method (driving, public_transport, walking, etc.)
        properties: Data to return (route, travel_time, distance, fares)
        range: Optional departure time window for multiple journey options
        snapping: Optional road network lookup settings
    """

    id: str
    arrival_location_ids: List[str]
    departure_location_id: str
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
    snapping: Optional[Snapping] = None


class RoutesRequest(TravelTimeRequest[RoutesResponse]):
    """
    Calculates A to B routes with turn-by-turn directions between specific locations.
    Best used for navigation and route visualization rather than catchment analysis.

    Attributes:
        locations: List of all locations referenced by ID in searches
        departure_searches: List of departure-based route searches (max 10)
        arrival_searches: List of arrival-based route searches (max 10)
    """

    locations: List[Location]
    departure_searches: List[RoutesDepartureSearch]
    arrival_searches: List[RoutesArrivalSearch]

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        return [
            RoutesRequest(
                locations=self.locations,
                departure_searches=departures,
                arrival_searches=arrivals,
            )
            for departures, arrivals in split(
                self.departure_searches, self.arrival_searches, window_size
            )
        ]

    def merge(self, responses: List[RoutesResponse]) -> RoutesResponse:
        return RoutesResponse(
            results=flatten([response.results for response in responses])
        )
