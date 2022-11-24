from abc import ABC
from dataclasses import dataclass


class Transportation(ABC):
    type: str


@dataclass(frozen=True)
class Driving(Transportation):
    type: str = 'driving'


@dataclass(frozen=True)
class Bus(Transportation):
    type: str = 'bus'


@dataclass(frozen=True)
class PublicTransport(Transportation):
    type: str = 'public_transport'
