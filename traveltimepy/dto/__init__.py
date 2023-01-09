from typing import NewType

from pydantic.main import BaseModel

SearchId = NewType('SearchId', str)
LocationId = NewType('LocationId', str)


class Coordinates(BaseModel):
    lat: float
    lng: float

    def __hash__(self):
        return hash(self.lat) ^ hash(self.lng)


class Location(BaseModel):
    id: LocationId
    coords: Coordinates

    def __hash__(self):
        return hash(self.id) ^ hash(self.coords)
