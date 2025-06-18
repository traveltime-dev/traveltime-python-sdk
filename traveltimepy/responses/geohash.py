from typing import List, Optional

from pydantic.main import BaseModel


class Properties(BaseModel):
    """
    Travel time statistics for a geohash cell.

    Contains optional minimum, maximum, and mean travel times in seconds
    for points of interest within the geohash cell.

    Attributes:
        min: Minimum travel time to any point of interest within the geohash cell, in seconds.
        max: Maximum travel time to any point of interest within the geohash cell, in seconds.
        mean: Mean travel time to points of interest within the geohash cell, in seconds.
    """

    min: Optional[int] = None
    max: Optional[int] = None
    mean: Optional[int] = None


class Cell(BaseModel):
    """
    Represents a single geohash cell with its travel time statistics.

    Attributes:
        id: Geohash string identifier for this geographic cell.
        properties: Travel time statistics for this cell.
    """

    id: str
    properties: Properties


class GeoHashResult(BaseModel):
    """
    Contains geohash analysis results for a single search operation.

    Attributes:
        search_id: Identifier matching the search ID from the original request.
                  Links the result back to the specific search operation that generated it.
        cells: List of geohash cells within the travel time catchment area.
              Each cell contains travel time statistics based on the requested properties.
    """

    search_id: str
    cells: List[Cell]


class GeoHashResponse(BaseModel):
    """
    Contains results for all searches, intersections, and unions requested in a single geohash analysis call.

    Attributes:
        results: List of all geohash analysis results. Contains one result per search operation
                (departure, arrival, intersection, union). Results are sorted lexicographically
                by search_id for consistent ordering.
    """

    results: List[GeoHashResult]
