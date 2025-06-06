from typing import List, Optional

from pydantic import BaseModel, field_serializer

from traveltimepy.dto.common import Location, Property, Snapping
from traveltimepy.dto.requests.request import TravelTimeRequest
from traveltimepy.dto.responses.time_filter_fast import TimeFilterFastResponse
from traveltimepy.dto.transportation_fast import TransportationFast
from traveltimepy.itertools import split, flatten


class TimeFilterFastOneToMany(BaseModel):
    id: str
    departure_location_id: str
    arrival_location_ids: List[str]
    transportation: TransportationFast
    travel_time: int
    arrival_time_period: str
    properties: List[Property]
    snapping: Optional[Snapping]
    
    # JSON expects `"transportation": { "type": "public_transport" }` and not `"transportation": "public_transport"`
    @field_serializer('transportation')
    def serialize_transportation(self, value: TransportationFast) -> dict:
        return {"type": value.value}


class TimeFilterFastManyToOne(BaseModel):
    id: str
    arrival_location_id: str
    departure_location_ids: List[str]
    transportation: TransportationFast
    travel_time: int
    arrival_time_period: str
    properties: List[Property]
    snapping: Optional[Snapping]
    
    # JSON expects `"transportation": { "type": "public_transport" }` and not `"transportation": "public_transport"`
    @field_serializer('transportation')
    def serialize_transportation(self, value: TransportationFast) -> dict:
        return {"type": value.value}


class TimeFilterFastArrivalSearches(BaseModel):
    many_to_one: List[TimeFilterFastManyToOne]
    one_to_many: List[TimeFilterFastOneToMany]


class TimeFilterFastRequest(TravelTimeRequest[TimeFilterFastResponse]):
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
