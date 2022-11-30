from datetime import datetime
from typing import List, Optional

from pydantic.main import BaseModel


class PublicTransport(BaseModel):
    date_start: datetime
    date_end: datetime


class Features(BaseModel):
    fares: bool
    postcodes: bool
    public_transport: Optional[PublicTransport]


class Map(BaseModel):
    name: str
    features: Features


class MapInfoResponse(BaseModel):
    maps: List[Map]
