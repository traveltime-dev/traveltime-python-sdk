from typing import List

from pydantic import BaseModel


class H3FastProtoResponse(BaseModel):
    """
    Attributes:
        ids: List of H3 cell indices in the same lowercase hex form the JSON h3
            endpoint returns, e.g. ``87194ad14ffffff``.
        min_travel_times: List of minimum travel times in seconds for each cell.
        max_travel_times: List of maximum travel times in seconds for each cell.
        mean_travel_times: List of mean travel times in seconds for each cell.
    """

    ids: List[str]
    min_travel_times: List[int]
    max_travel_times: List[int]
    mean_travel_times: List[int]
