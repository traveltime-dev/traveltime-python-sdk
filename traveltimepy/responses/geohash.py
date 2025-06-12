from typing import List, Optional

from pydantic.main import BaseModel


class Properties(BaseModel):
    """
    Travel time statistics for a geohash cell.

    Contains optional minimum, maximum, and mean travel times in seconds
    for points of interest within the geohash cell.
    """

    min: Optional[int] = None
    """Minimum travel time to any point of interest within the geohash cell, in seconds."""

    max: Optional[int] = None
    """Maximum travel time to any point of interest within the geohash cell, in seconds."""

    mean: Optional[int] = None
    """Average travel time to points of interest within the geohash cell, in seconds."""


class Cell(BaseModel):
    """
    Represents a single geohash cell with its travel time statistics.
    """

    id: str
    """Geohash string identifier for this geographic cell."""

    properties: Properties
    """Travel time statistics for this cell."""


class GeoHashResult(BaseModel):
    """
    Contains geohash analysis results for a single search operation.
    """

    search_id: str
    """
    Identifier matching the search ID from the original request.
    Links the result back to the specific search operation that generated it.
    """

    cells: List[Cell]
    """
    List of geohash cells within the travel time catchment area.
    Each cell contains travel time statistics based on the requested properties.
    """


class GeoHashResponse(BaseModel):
    """
    Contains results for all searches, intersections, and unions requested in a single geohash analysis call.
    """

    results: List[GeoHashResult]
    """
    List of all geohash analysis results.
    Contains one result per search operation (departure, arrival, intersection, union).
    Results are sorted lexicographically by search_id for consistent ordering.
    """
