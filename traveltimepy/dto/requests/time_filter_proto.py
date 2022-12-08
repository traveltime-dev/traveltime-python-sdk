from enum import Enum
from typing import List

from pydantic import BaseModel
from traveltimepy.dto import Coordinates


class Transportation(str, Enum):
    PUBLIC_TRANSPORT = 'pt'
    WALKING_FERRY = 'walking+ferry'


class Country(str, Enum):
    NETHERLANDS = 'nl'
    AUSTRIA = 'at'


class OneToMany(BaseModel):
    origin_coordinates: Coordinates
    destination_coordinates: List[Coordinates]
    transportation: Transportation
    travel_time: int
    country: Country
