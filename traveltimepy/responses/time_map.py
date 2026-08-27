from typing import List, Optional

from pydantic.main import BaseModel

from traveltimepy.requests.common import Coordinates


class Shape(BaseModel):
    """Polygon shape representing a reachable area within a catchment analysis result.

    Attributes:
        shell: Outer boundary coordinates forming the main polygon perimeter.
        holes: Inner boundaries representing unreachable areas within the main shape.
    """

    shell: List[Coordinates]
    holes: List[List[Coordinates]]


class TimeMapProperties(BaseModel):
    """Additional properties returned for a time-map result when requested.

    Attributes:
        is_only_walking: Whether the reachable area is walking-only.
    """

    is_only_walking: Optional[bool] = None


class TimeMapResult(BaseModel):
    """Catchment area calculation result for a single search operation.

    Attributes:
        search_id: Search identifier from the original request.
        shapes: Collection of polygon shapes defining the reachable area.
        properties: Additional properties, present when requested.
    """

    search_id: str
    shapes: List[Shape]
    properties: Optional[TimeMapProperties] = None


class TimeMapResponse(BaseModel):
    """
    Attributes:
        results: List of all catchment area calculation results.
    """

    results: List[TimeMapResult]
