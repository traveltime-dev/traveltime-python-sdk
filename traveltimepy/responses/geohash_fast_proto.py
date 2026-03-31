from typing import List

from pydantic import BaseModel


class GeohashFastProtoResponse(BaseModel):
    """
    Attributes:
        ids: List of geohash cell IDs.
        min_travel_times: List of minimum travel times in seconds for each cell.
        max_travel_times: List of maximum travel times in seconds for each cell.
        mean_travel_times: List of mean travel times in seconds for each cell.
    """

    ids: List[str]
    min_travel_times: List[int]
    max_travel_times: List[int]
    mean_travel_times: List[int]
