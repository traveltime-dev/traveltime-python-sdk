from typing import List

from pydantic.main import BaseModel

from traveltimepy.requests.common import Coordinates


class Shape(BaseModel):
    """
    Polygon shape representing a reachable area within a catchment analysis result.

    Attributes:
        shell: Outer boundary coordinates forming the main polygon perimeter.
        holes: Inner boundaries representing unreachable areas within the main shape.
    """

    shell: List[Coordinates]
    holes: List[List[Coordinates]]


class TimeMapResult(BaseModel):
    """
    Catchment area calculation result for a single search operation.

    Attributes:
        search_id: Search identifier from the original request.
        shapes: Collection of polygon shapes defining the reachable area.
    """

    search_id: str
    shapes: List[Shape]


class TimeMapResponse(BaseModel):
    """
    Attributes:
        results: List of all catchment area calculation results.
    """

    results: List[TimeMapResult]
