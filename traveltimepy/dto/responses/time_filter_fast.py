from typing import List, Optional
from pydantic import BaseModel


class Ticket(BaseModel):
    type: str
    price: float
    currency: str


class Fares(BaseModel):
    tickets_total: List[Ticket]


class Properties(BaseModel):
    travel_time: int
    fares: Optional[Fares]


class Location(BaseModel):
    id: str
    properties: Properties


class TimeFilterFastResult(BaseModel):
    search_id: str
    locations: List[Location]
    unreachable: List[str]


class TimeFilterFastResponse(BaseModel):
    results: List[TimeFilterFastResult]
