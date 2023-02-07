from typing import List
from typing_extensions import Literal

from pydantic import BaseModel

from traveltimepy.dto.common import Location, Property
from traveltimepy.dto.requests.request import TravelTimeRequest
from traveltimepy.dto.responses.time_filter_fast import TimeFilterFastResponse
from traveltimepy.itertools import split, flatten


class Transportation(BaseModel):
    type: Literal[
        'public_transport',
        'driving',
        'cycling',
        'walking',
        'walking+ferry',
        'cycling+ferry',
        'driving+ferry',
        'driving+public_transport'
    ]


class OneToMany(BaseModel):
    id: str
    departure_location_id: str
    arrival_location_ids: List[str]
    transportation: Transportation
    travel_time: int
    arrival_time_period: str
    properties: List[Property]


class ManyToOne(BaseModel):
    id: str
    arrival_location_id: str
    departure_location_ids: List[str]
    transportation: Transportation
    travel_time: int
    arrival_time_period: str
    properties: List[Property]


class ArrivalSearches(BaseModel):
    many_to_one: List[ManyToOne]
    one_to_many: List[OneToMany]


class TimeFilterFastRequest(TravelTimeRequest[TimeFilterFastResponse]):
    locations: List[Location]
    arrival_searches: ArrivalSearches

    def split_searches(self) -> List[TravelTimeRequest]:
        return [
            TimeFilterFastRequest(
                locations=self.locations,
                arrival_searches=ArrivalSearches(
                    one_to_many=one_to_many,
                    many_to_one=many_to_one
                )
            )
            for one_to_many, many_to_one in split(self.arrival_searches.one_to_many, self.arrival_searches.many_to_one, 10)
        ]

    def merge(self, responses: List[TimeFilterFastResponse]) -> TimeFilterFastResponse:
        return TimeFilterFastResponse(results=flatten([response.results for response in responses]))
