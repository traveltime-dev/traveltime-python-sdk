import time
import random
from datetime import datetime
from typing import List

from traveltimepy import Coordinates, Location, TravelTimeSdk, Driving


def generate_float(value: float, radius: float) -> float:
    return random.uniform(value - radius, value + radius)


def generate_locations(lat: float, lng: float, radius: float, name: str, amount: int) -> List[Location]:
    return [
        Location(
            id='{} {}'.format(name, i),
            coords=Coordinates(lat=generate_float(lat, radius), lng=generate_float(lng, radius))
        ) for i in range(amount)
    ]


def generate_matrix(size: int):
    sdk = TravelTimeSdk('APP_ID', 'API_KEY')
    locations = generate_locations(51.507609, -0.128315, 0.05, 'Location', size)
    location_ids = [location.id for location in locations]
    searches = [
        (location_id, list(filter(lambda cur_id: cur_id != location_id, location_ids)))
        for location_id in location_ids
    ]
    return sdk.time_filter(
        locations=locations,
        searches=dict(searches),
        transportation=Driving(),
        arrival_time=datetime.now(),
    )


if __name__ == '__main__':
    start = time.perf_counter()
    response = generate_matrix(50)
    request_time = time.perf_counter() - start
    print("Request completed in {0:.0f}s for matrix 50 * 50".format(request_time))

    start = time.perf_counter()
    response2 = generate_matrix(100)
    request_time = time.perf_counter() - start
    print("Request completed in {0:.0f}s for matrix 100 * 100".format(request_time))

    start = time.perf_counter()
    response3 = generate_matrix(300)
    request_time = time.perf_counter() - start
    print("Request completed in {0:.0f}s for matrix 300 * 300".format(request_time))