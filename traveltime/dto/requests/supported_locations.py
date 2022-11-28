from typing import List

from pydantic import BaseModel

from traveltime.dto import Location


class SupportedLocationsRequest(BaseModel):
    locations: List[Location]
