from typing import List, Optional

from pydantic.main import BaseModel


class Properties(BaseModel):
    """
    Travel time statistics for an H3 hexagonal cell.

    Contains optional minimum, maximum, and mean travel times in seconds
    for points of interest within the H3 cell. H3 is hexagonal
    hierarchical spatial indexing system.

    Attributes:
        min: Minimum travel time to any point of interest within the H3 cell, in seconds.
        max: Maximum travel time to any point of interest within the H3 cell, in seconds.
        mean: Mean travel time to points of interest within the H3 cell, in seconds.
    """

    min: Optional[int] = None
    max: Optional[int] = None
    mean: Optional[int] = None


class Cell(BaseModel):
    """
    Represents a single H3 hexagonal cell with its travel time statistics.

    Attributes:
        id: H3 cell identifier string for this hexagonal geographic cell.
        properties: Travel time statistics calculated for this cell.
    """

    id: str
    properties: Properties


class H3Result(BaseModel):
    """
    Contains H3 hexagonal cell analysis results for a single search operation.

    Each result corresponds to one search (departure, arrival, intersection, or union)
    and contains all H3 cells within the travel time catchment area for that search.

    Attributes:
        search_id: Identifier matching the search ID from the original request.
                  Links the result back to the specific search operation that generated it.
        cells: List of H3 hexagonal cells within the travel time catchment area.
              Each cell contains travel time statistics based on the requested properties.
    """

    search_id: str
    cells: List[Cell]


class H3Response(BaseModel):
    """
    Contains results for all H3 searches, intersections, and unions requested in a single analysis call.

    The response includes travel time data for H3 hexagonal cells within catchment areas,
    with statistical information (min/max/mean) for each cell based on the requested properties.

    Attributes:
        results: List of all H3 analysis results. Contains one result per search operation
                (departure, arrival, intersection, union). Results are sorted lexicographically
                by search_id for consistent ordering.
    """

    results: List[H3Result]
