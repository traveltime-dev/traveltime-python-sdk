from typing import List
from typing_extensions import Literal

from pydantic import BaseModel

from traveltimepy.dto import LocationId, Location
from traveltimepy.dto.requests import Property


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
    departure_location_id: LocationId
    arrival_location_ids: List[LocationId]
    transportation: Transportation
    travel_time: int
    arrival_time_period: str
    properties: List[Property]


class ManyToOne(BaseModel):
    id: str
    arrival_location_id: LocationId
    departure_location_ids: List[LocationId]
    transportation: Transportation
    travel_time: int
    arrival_time_period: str
    properties: List[Property]


class ArrivalSearches(BaseModel):
    many_to_one: List[ManyToOne]
    one_to_many: List[OneToMany]


class TimeFilterFastRequest(BaseModel):
    locations: List[Location]
    arrival_searches: ArrivalSearches
