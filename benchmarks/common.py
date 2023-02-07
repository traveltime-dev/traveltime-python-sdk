import random
from typing import List

from traveltimepy import Location, Coordinates


def generate_float(value: float, radius: float) -> float:
    return random.uniform(value - radius, value + radius)


def generate_locations(lat: float, lng: float, radius: float, name: str, amount: int) -> List[Location]:
    return [
        Location(
            id='{} {}'.format(name, i),
            coords=Coordinates(lat=generate_float(lat, radius), lng=generate_float(lng, radius))
        ) for i in range(amount)
    ]


def generate_coordinates(lat: float, lng: float, radius: float, amount: int) -> List[Coordinates]:
    return [Coordinates(lat=generate_float(lat, radius), lng=generate_float(lng, radius)) for _ in range(amount)]
