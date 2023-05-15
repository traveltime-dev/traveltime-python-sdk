from dataclasses import dataclass
from enum import Enum


@dataclass
class TransportationInfo:
    code: int
    name: str


class ProtoTransportation(Enum):
    PUBLIC_TRANSPORT = TransportationInfo(0, "pt")
    DRIVING_FERRY = TransportationInfo(3, "driving+ferry")
    CYCLING_FERRY = TransportationInfo(6, "cycling+ferry")
    WALKING_FERRY = TransportationInfo(7, "walking+ferry")


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
