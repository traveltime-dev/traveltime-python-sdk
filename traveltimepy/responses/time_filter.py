from typing import List, Optional

from pydantic.main import BaseModel

from traveltimepy.requests.common import Route, Fares


class DistanceBreakdown(BaseModel):
    """
    Distance breakdown by transportation mode.

    Attributes:
        mode: Transportation mode (e.g., walking, driving).
        distance: Distance in meters for this mode.
    """

    mode: str
    distance: int


class TimeFilterProperty(BaseModel):
    """
    Travel statistics for a distance matrix destination.

    Attributes:
        travel_time: Journey time in seconds.
        distance: Total journey distance in meters.
        distance_breakdown: Distance breakdown by transportation mode.
        fares: Public transport fare information.
        route: Detailed route with turn-by-turn directions.
    """

    travel_time: int
    distance: Optional[int] = None
    distance_breakdown: Optional[List[DistanceBreakdown]] = None
    fares: Optional[Fares] = None
    route: Optional[Route] = None


class Location(BaseModel):
    """
    Destination location with travel statistics.

    Attributes:
        id: Location identifier from the original request.
        properties: Travel statistics for journeys to this location.
    """

    id: str
    properties: List[TimeFilterProperty]


class TimeFilterResult(BaseModel):
    """
    Distance matrix results for a single search operation.

    Attributes:
        search_id: Search identifier from the original request.
        locations: Destination locations with travel statistics.
        unreachable: Location IDs that could not be reached.
    """

    search_id: str
    locations: List[Location]
    unreachable: List[str]


class TimeFilterResponse(BaseModel):
    """
    Results for all distance matrix searches with travel times and distances.

    Attributes:
        results: List of distance matrix results, one per search operation.
    """

    results: List[TimeFilterResult]
