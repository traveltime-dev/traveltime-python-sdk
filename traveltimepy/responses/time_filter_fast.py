from typing import List, Optional
from pydantic import BaseModel


class Ticket(BaseModel):
    """
    Public transport ticket information.

    Attributes:
        type: Ticket type (e.g., single, day, week).
        price: Ticket price amount.
        currency: Currency code (e.g., GBP, USD).
    """

    type: str
    price: float
    currency: str


class Fares(BaseModel):
    """
    Public transport fare breakdown.

    Attributes:
        tickets_total: List of tickets required for the journey.
    """

    tickets_total: List[Ticket]


class Properties(BaseModel):
    """
    Travel statistics for a high-performance distance matrix destination.

    Attributes:
        travel_time: Journey time in seconds.
        distance: Journey distance in meters.
        fares: Public transport fare information.
    """

    travel_time: int
    distance: Optional[int] = None
    fares: Optional[Fares] = None


class Location(BaseModel):
    """
    Destination location with travel statistics.

    Attributes:
        id: Location identifier from the original request.
        properties: Travel statistics for this destination.
    """

    id: str
    properties: Properties


class TimeFilterFastResult(BaseModel):
    """
    High-performance distance matrix results for a single search operation.

    Attributes:
        search_id: Search identifier from the original request.
        locations: Destination locations with travel statistics.
        unreachable: Location IDs that could not be reached.
    """

    search_id: str
    locations: List[Location]
    unreachable: List[str]


class TimeFilterFastResponse(BaseModel):
    """
    Attributes:
        results: List of distance matrix results, one per search operation.
    """

    results: List[TimeFilterFastResult]
