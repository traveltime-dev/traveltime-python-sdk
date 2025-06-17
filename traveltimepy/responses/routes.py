from typing import List, Optional

from pydantic.main import BaseModel

from traveltimepy.requests.common import Fares, Route


class RoutesProperty(BaseModel):
    """
    Travel statistics and route information for an A to B journey.

    Attributes:
        travel_time: Journey time in seconds.
        fares: Public transport fare information.
        distance: Journey distance in meters.
        route: Detailed route with turn-by-turn directions.
    """

    travel_time: Optional[int] = None
    fares: Optional[Fares] = None
    distance: Optional[int] = None
    route: Optional[Route] = None


class Location(BaseModel):
    """
    Destination location with route properties.

    Attributes:
        id: Location identifier from the original request.
        properties: Route properties for journeys to this location.
    """

    id: str
    properties: List[RoutesProperty]


class RoutesResult(BaseModel):
    """
    A to B route analysis results for a single search operation.

    Attributes:
        search_id: Search identifier from the original request.
        locations: Destination locations with route properties.
        unreachable: Location IDs that could not be reached.
    """

    search_id: str
    locations: List[Location]
    unreachable: List[str]


class RoutesResponse(BaseModel):
    """
    Results for all A to B route searches with turn-by-turn directions.

    Attributes:
        results: List of route analysis results, one per search operation.
    """

    results: List[RoutesResult]
