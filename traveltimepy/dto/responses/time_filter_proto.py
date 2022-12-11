from typing import List

from pydantic import BaseModel


class TimeFilterProtoResponse(BaseModel):
    travel_times: List[int]
