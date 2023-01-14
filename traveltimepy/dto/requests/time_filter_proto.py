from dataclasses import dataclass
from enum import Enum


@dataclass
class TransportationInfo:
    code: int
    name: str


class ProtoTransportation(Enum):
    PUBLIC_TRANSPORT = TransportationInfo(0, 'pt')
    DRIVING = TransportationInfo(1, 'driving')
    DRIVING_FERRY = TransportationInfo(3, 'driving+ferry')
    WALKING = TransportationInfo(4, 'walking')
    CYCLING = TransportationInfo(5, 'cycling')
    CYCLING_FERRY = TransportationInfo(6, 'cycling+ferry')
    WALKING_FERRY = TransportationInfo(7, 'walking+ferry')


class ProtoCountry(str, Enum):
    NETHERLANDS = 'nl'
    AUSTRIA = 'at'
    UNITED_KINGDOM = 'uk'
    BELGIUM = 'be'
    GERMANY = 'de'
    FRANCE = 'fr'
    IRELAND = 'ie'
    LITHUANIA = 'lt'
