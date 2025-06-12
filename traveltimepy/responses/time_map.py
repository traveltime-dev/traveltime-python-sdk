from typing import List

from pydantic.main import BaseModel

from traveltimepy.requests.common import Coordinates


class Shape(BaseModel):
    """
    A polygon shape representing a reachable area within a distance map result.
    """

    shell: List[Coordinates]
    """
    Outer boundary coordinates forming the main polygon perimeter.
    """

    holes: List[List[Coordinates]]
    """
    Inner boundaries representing unreachable areas within the main shape.
    Each hole is a closed polygon. Can be removed using 'no_holes' parameter.
    """


class TimeMapResult(BaseModel):
    """
    Distance map calculation result for a single search operation.
    """

    search_id: str
    """
    Identifier matching the search ID from the original request.
    Links the result back to the specific search operation that generated it.
    """

    shapes: List[Shape]
    """
    Collection of polygon shapes defining the reachable area.
    """


class TimeMapResponse(BaseModel):
    """
    Complete response from a distance map API request.
    """

    results: List[TimeMapResult]
    """
    List of all distance map calculation results.
    """
