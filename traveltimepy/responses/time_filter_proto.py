from typing import List

from pydantic import BaseModel


class TimeFilterProtoResponse(BaseModel):
    """
    Attributes:
        travel_times: List of travel times in seconds for each destination.
        distances: List of distances in meters for each destination (if requested).
    """

    travel_times: List[int]
    distances: List[int]
