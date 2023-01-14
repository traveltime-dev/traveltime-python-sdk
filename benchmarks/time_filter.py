import asyncio
import time
import random
from datetime import datetime
from typing import List

from traveltimepy import Coordinates, Location, Range
from traveltimepy.dto.requests import Range
from traveltimepy.dto.requests.time_filter import DepartureSearch
from traveltimepy.sdk import TravelTimeSdk
from traveltimepy.dto.transportation import PublicTransport


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
    sdk = TravelTimeSdk("APP_ID", "API_KEY")
    locations = generate_locations(51.507609, -0.128315, 0.05, 'Location', 50)
    location_ids = [location.id for location in locations]
    searches = [
        (location_id, list(filter(lambda cur_id: cur_id != location_id, location_ids)))
        for location_id in location_ids
    ]
    return await sdk.time_filter_async(
        locations=locations,
        searches=dict(searches),
        transportation=PublicTransport(),
        arrival_time=datetime.now(),
    )


if __name__ == '__main__':
    start = time.perf_counter()
    response = asyncio.run(send())
    print(response.results)
    request_time = time.perf_counter() - start
    print("Request completed in {0:.0f}s".format(request_time))
