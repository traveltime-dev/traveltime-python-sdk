from typing import List

from pydantic import BaseModel

from traveltimepy.dto import Location


class SupportedLocationsRequest(BaseModel):
    locations: List[Location]
