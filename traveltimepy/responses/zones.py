from typing import List, Optional

from pydantic import BaseModel


class TravelTime(BaseModel):
    """
    Travel time statistics in seconds.

    Attributes:
        min: Minimum travel time.
        max: Maximum travel time.
        mean: Mean travel time.
        median: Median travel time.
    """

    min: int
    max: int
    mean: int
    median: int


class Properties(BaseModel):
    """
    Travel time statistics and coverage for a postcode zone.

    Attributes:
        travel_time_reachable: Statistics for reachable postcodes within the zone.
        travel_time_all: Statistics for all postcodes within the zone.
        coverage: Percentage of reachable postcodes in the zone (0.0-1.0).
    """

    travel_time_reachable: Optional[TravelTime] = None
    travel_time_all: Optional[TravelTime] = None
    coverage: Optional[float] = None


class Zone(BaseModel):
    """
    Postcode sector or district with travel statistics.

    Attributes:
        code: Postcode sector or district code.
        properties: Travel time statistics and coverage data.
    """

    code: str
    properties: Properties


class PostcodesSectorsResult(BaseModel):
    """
    Postcode sectors analysis result for a single search operation.

    Attributes:
        search_id: Search identifier from the original request.
        sectors: List of postcode sectors with travel statistics.
    """

    search_id: str
    sectors: List[Zone]


class PostcodesDistrictsResult(BaseModel):
    """
    Postcode districts analysis result for a single search operation.

    Attributes:
        search_id: Search identifier from the original request.
        districts: List of postcode districts with travel statistics.
    """

    search_id: str
    districts: List[Zone]


class PostcodesSectorsResponse(BaseModel):
    """
    Results for all postcode sectors searches with coverage filtering.

    Attributes:
        results: List of sector analysis results, one per search operation.
    """

    results: List[PostcodesSectorsResult]


class PostcodesDistrictsResponse(BaseModel):
    """
    Results for all postcode districts searches with coverage filtering.

    Attributes:
        results: List of district analysis results, one per search operation.
    """

    results: List[PostcodesDistrictsResult]
