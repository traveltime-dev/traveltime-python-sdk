from dataclasses import dataclass
from enum import Enum
from typing import ClassVar, Optional


@dataclass
class TransportationInfo:
    code: int
    name: str


class ProtoTransportation(Enum):
    PUBLIC_TRANSPORT = TransportationInfo(0, "pt")
    DRIVING = TransportationInfo(1, "driving")
    DRIVING_AND_PUBLIC_TRANSPORT = TransportationInfo(2, "pt")
    DRIVING_FERRY = TransportationInfo(3, "driving+ferry")
    WALKING = TransportationInfo(4, "walking")
    CYCLING = TransportationInfo(5, "cycling")
    CYCLING_FERRY = TransportationInfo(6, "cycling+ferry")
    WALKING_FERRY = TransportationInfo(7, "walking+ferry")


@dataclass
class PublicTransportWithDetails:

    walking_time_to_station: Optional[int] = None
    """Limit on walking path duration. Must be <= 1800"""

    TYPE: ClassVar[ProtoTransportation] = ProtoTransportation.PUBLIC_TRANSPORT


@dataclass
class DrivingAndPublicTransportWithDetails:

    walking_time_to_station: Optional[int] = None
    """Limit on walking path duration. Must be <= 1800"""

    driving_time_to_station: Optional[int] = None
    """Limit on driving path duration. Must be <= 1800"""

    parking_time: Optional[int] = None
    """
    Constant penalty to simulate finding a parking spot in seconds.
    Must be less than the overall travel time limit.
    """

    TYPE: ClassVar[ProtoTransportation] = (
        ProtoTransportation.DRIVING_AND_PUBLIC_TRANSPORT
    )


class ProtoCountry(str, Enum):
    NETHERLANDS = "nl"
    AUSTRIA = "at"
    UNITED_KINGDOM = "uk"
    BELGIUM = "be"
    GERMANY = "de"
    FRANCE = "fr"
    IRELAND = "ie"
    LITHUANIA = "lt"
    UNITED_STATES = "us"
    SOUTH_AFRICA = "za"
    ROMANIA = "ro"
    PORTUGAL = "pt"
    PHILIPPINES = "ph"
    NEW_ZEALAND = "nz"
    NORWAY = "no"
    LATVIA = "lv"
    JAPAN = "jp"
    INDIA = "in"
    INDONESIA = "id"
    HUNGARY = "hu"
    GREECE = "gr"
    FINLAND = "fi"
    DENMARK = "dk"
    CANADA = "ca"
    AUSTRALIA = "au"
    SINGAPORE = "sg"
    SWITZERLAND = "ch"
    SPAIN = "es"
    ITALY = "it"
    POLAND = "pl"
    SWEDEN = "se"
    LIECHTENSTEIN = "li"
    MEXICO = "mx"
    SAUDI_ARABIA = "sa"
    SERBIA = "rs"
    SLOVENIA = "si"
