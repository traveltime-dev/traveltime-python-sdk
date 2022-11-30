from typing import NewType

from pydantic.main import BaseModel

SearchId = NewType('SearchId', str)
LocationId = NewType('LocationId', str)


class Coordinates(BaseModel):
    lat: float
    lng: float


class Location(BaseModel):
    id: LocationId
    coords: Coordinates
