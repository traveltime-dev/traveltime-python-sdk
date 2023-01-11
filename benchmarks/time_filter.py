import asyncio
import time
import random
from datetime import datetime
from typing import List

from traveltimepy.dto import Coordinates, Location
from traveltimepy.dto.requests import Range, Property
from traveltimepy.dto.requests.time_filter import DepartureSearch
from traveltimepy.sdk import TravelTimeSdk
from traveltimepy.transportation import PublicTransport


def generate_float(value: float, radius: float) -> float:
    return random.uniform(value - radius, value + radius)


def generate_locations(lat: float, lng: float, radius: float, name: str, amount: int) -> List[Location]:
    return [
        Location(
            id='{} {}'.format(name, i),
            coords=Coordinates(lat=generate_float(lat, radius), lng=generate_float(lng, radius))
        ) for i in range(amount)
    ]


"""

def generate_searches(coordinates: List[Coordinates]):
    return [
        ArrivalSearch(
            id="search for {}".format(coordinate),
            coords=coordinate,
            arrival_time=datetime.now(),
            travel_time=900,
            transportation=PublicTransport(),
            range=Range(enabled=True, width=3600)
        )
        for coordinate in coordinates
    ]

"""


def generate_departures(coordinates: List[Coordinates]):
    return [
        DepartureSearch(
            id="search for {}".format(coordinate),
            coords=coordinate,
            arrival_time=datetime.now(),
            travel_time=900,
            transportation=PublicTransport(),
            range=Range(enabled=True, width=3600)
        )
        for coordinate in coordinates
    ]


async def send():
    sdk = TravelTimeSdk("", "")
    locations: List[Location] = generate_locations(51.507609, -0.128315, 0.05, 'Location', 50)
    all_locations = [(location, list(filter(lambda cur: cur.id != location.id, locations))) for location in locations]
    return await sdk.time_filter_async(
        locations=dict(all_locations),
        transportation=PublicTransport(),
        arrival_time=datetime.now(),
    )


if __name__ == '__main__':
    start = time.perf_counter()
    response = asyncio.run(send())
    print(response.results)
    request_time = time.perf_counter() - start
    print("Request completed in {0:.0f}s".format(request_time))
