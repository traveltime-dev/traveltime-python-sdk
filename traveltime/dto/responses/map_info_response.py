from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass(frozen=True)
class PublicTransport:
    date_start: datetime
    date_end: datetime


@dataclass(frozen=True)
class Features:
    fares: bool
    postcodes: bool
    public_transport: Optional[PublicTransport]


@dataclass(frozen=True)
class Map:
    name: str
    features: Features


@dataclass(frozen=True)
class MapInfoResponse:
    maps: List[Map]
