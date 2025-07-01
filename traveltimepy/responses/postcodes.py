from typing import List, Optional

from pydantic import BaseModel


class PostcodeProperty(BaseModel):
    """
    Travel statistics for a postcode.

    Contains optional travel time and distance data for reaching or departing from a specific postcode.

    Attributes:
        travel_time: Journey time to/from this postcode in seconds.
        distance: Journey distance to/from this postcode in meters.
    """

    travel_time: Optional[int] = None
    distance: Optional[int] = None


class Postcode(BaseModel):
    """
    Represents a single postcode with its travel statistics.

    Attributes:
        code: postcode string identifier (e.g., "SW1A 1AA").
        properties: List of travel statistics for this postcode. May contain
                   multiple entries when range searches return alternative journey options.
    """

    code: str
    properties: List[PostcodeProperty]


class PostcodesResult(BaseModel):
    """
    Contains postcode analysis results for a single search operation.

    Each result corresponds to one search (departure or arrival) and contains
    all reachable postcodes within the travel time catchment area for that search.

    Attributes:
        search_id: Identifier matching the search ID from the original request.
                  Links the result back to the specific search operation that generated it.
        postcodes: List of postcodes within the travel time catchment area.
                  Each postcode contains travel statistics based on the requested properties.
    """

    search_id: str
    postcodes: List[Postcode]


class PostcodesResponse(BaseModel):
    """
    Contains results for all postcode searches requested in a single analysis call.

    The response includes travel time and distance data for postcodes within catchment areas.

    Attributes:
        results: List of all postcode analysis results. Contains one result per search operation
                (departure or arrival). Results are sorted lexicographically by search_id
                for consistent ordering.
    """

    results: List[PostcodesResult]
