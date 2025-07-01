from typing import List, Optional

from pydantic import BaseModel, field_serializer

from traveltimepy.requests.transportation import TransportationFast
from traveltimepy.requests.common import Location, Property, Snapping, ArrivalTimePeriod
from traveltimepy.requests.request import TravelTimeRequest
from traveltimepy.responses.time_filter_fast import TimeFilterFastResponse
from traveltimepy.itertools import split, flatten


class TimeFilterFastOneToMany(BaseModel):
    """
    One-to-many travel time search for high-performance distance matrix calculation.

    Calculates travel times from a single departure location to multiple arrival
    locations with optimized performance for large datasets.

    Attributes:
        id: Unique identifier for this search
        departure_location_id: Single departure location ID
        arrival_location_ids: List of arrival location IDs (up to 100,000 destinations)
        transportation: Transportation mode
        travel_time: Maximum journey time in seconds (max 10,800 = 3 hours)
        properties: Data to return (travel_time, distance, fares)
        arrival_time_period: Time period instead of specific time
        snapping: Optional road network lookup settings
    """

    id: str
    departure_location_id: str
    arrival_location_ids: List[str]
    transportation: TransportationFast
    travel_time: int
    properties: List[Property]
    arrival_time_period: ArrivalTimePeriod = ArrivalTimePeriod.WEEKDAY_MORNING
    snapping: Optional[Snapping] = None

    # JSON expects `"transportation": { "type": "public_transport" }` and not `"transportation": "public_transport"`
    @field_serializer("transportation")
    def serialize_transportation(self, value: TransportationFast) -> dict:
        return {"type": value.value}


class TimeFilterFastManyToOne(BaseModel):
    """
    Many-to-one travel time search for high-performance distance matrix calculation.

    Calculates travel times from multiple departure locations to a single arrival
    location with optimized performance for large datasets.

    Attributes:
        id: Unique identifier for this search
        arrival_location_id: Single arrival location ID
        departure_location_ids: List of departure location IDs (up to 100,000 origins)
        transportation: Transportation mode
        travel_time: Maximum journey time in seconds (max 10,800 = 3 hours)
        properties: Data to return (travel_time, distance, fares)
        arrival_time_period: Time period instead of specific time
        snapping: Optional road network lookup settings
    """

    id: str
    arrival_location_id: str
    departure_location_ids: List[str]
    transportation: TransportationFast
    travel_time: int
    properties: List[Property]
    arrival_time_period: ArrivalTimePeriod = ArrivalTimePeriod.WEEKDAY_MORNING
    snapping: Optional[Snapping] = None

    # JSON expects `"transportation": { "type": "public_transport" }` and not `"transportation": "public_transport"`
    @field_serializer("transportation")
    def serialize_transportation(self, value: TransportationFast) -> dict:
        return {"type": value.value}


class TimeFilterFastArrivalSearches(BaseModel):
    """
    Attributes:
        many_to_one: Searches from multiple origins to single destinations
        one_to_many: Searches from single origins to multiple destinations
    """

    many_to_one: List[TimeFilterFastManyToOne]
    one_to_many: List[TimeFilterFastOneToMany]


class TimeFilterFastRequest(TravelTimeRequest[TimeFilterFastResponse]):
    """
    High-performance distance matrix endpoint optimized for large datasets with
    fewer configurable parameters but extremely low response times. Can handle
    up to 100,000 destinations in a single request.

    Attributes:
        locations: List of all locations referenced by ID in searches
        arrival_searches: Arrival-based search configurations for fast processing
    """

    locations: List[Location]
    arrival_searches: TimeFilterFastArrivalSearches

    def split_searches(self, window_size: int) -> List[TravelTimeRequest]:
        return [
            TimeFilterFastRequest(
                locations=self.locations,
                arrival_searches=TimeFilterFastArrivalSearches(
                    one_to_many=one_to_many, many_to_one=many_to_one
                ),
            )
            for one_to_many, many_to_one in split(
                self.arrival_searches.one_to_many,
                self.arrival_searches.many_to_one,
                window_size,
            )
        ]

    def merge(self, responses: List[TimeFilterFastResponse]) -> TimeFilterFastResponse:
        return TimeFilterFastResponse(
            results=flatten([response.results for response in responses])
        )
