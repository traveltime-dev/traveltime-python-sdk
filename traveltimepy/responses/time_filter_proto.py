from typing import List

from pydantic import BaseModel


class TimeFilterProtoResponse(BaseModel):
    """
    Attributes:
        travel_times: List of travel times in seconds for each destination.
        distances: List of distances in meters for each destination (if requested).
        monthly_fares: Monthly public transport ticket price for each destination, in
            minor currency units (e.g. pence), if requested. 0 where no fare is
            available or the destination is unreachable.
    """

    travel_times: List[int]
    distances: List[int]
    monthly_fares: List[int] = []
