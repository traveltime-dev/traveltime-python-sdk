from typing import List

from pydantic import BaseModel

from traveltimepy.dto import SearchId, LocationId


class Ticket(BaseModel):
    type: str
    price: float
    currency: str


class Fares(BaseModel):
    tickets_total: List[Ticket]


class Properties(BaseModel):
    travel_time: int
    fares: Fares


class Location(BaseModel):
    id: LocationId
    properties: Properties


class Result(BaseModel):
    search_id: SearchId
    locations: List[Location]
    unreachable: List[LocationId]


class TimeFilterFastResponse(BaseModel):
    results: List[Result]
