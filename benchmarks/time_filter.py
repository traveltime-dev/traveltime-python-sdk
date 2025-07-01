import asyncio
import time
from datetime import datetime

from benchmarks.common import generate_locations
from traveltimepy.requests.common import Property
from traveltimepy.requests.transportation import Driving
from traveltimepy.async_client import AsyncClient
from traveltimepy.requests.time_filter import TimeFilterDepartureSearch


async def generate_matrix(size: int):
    async with AsyncClient("APP_ID", "API_KEY") as async_client:
        locations = generate_locations(51.507609, -0.128315, 0.05, "Location", size)
        location_ids = [location.id for location in locations]
        searches = [
            TimeFilterDepartureSearch(
                id=location_id,
                departure_location_id=location_id,
                arrival_location_ids=list(
                    filter(lambda cur_id: cur_id != location_id, location_ids)
                ),
                departure_time=datetime.now(),
                transportation=Driving(),
                travel_time=3600,
                properties=[Property.TRAVEL_TIME],
            )
            for location_id in location_ids
        ]
        return await async_client.time_filter(
            locations=locations, departure_searches=searches, arrival_searches=[]
        )


if __name__ == "__main__":
    start = time.perf_counter()
    response = asyncio.run(generate_matrix(50))
    request_time = time.perf_counter() - start
    print("Request completed in {0:.0f}s for matrix 50 * 50".format(request_time))

    start = time.perf_counter()
    response2 = asyncio.run(generate_matrix(100))
    request_time = time.perf_counter() - start
    print("Request completed in {0:.0f}s for matrix 100 * 100".format(request_time))

    start = time.perf_counter()
    response3 = asyncio.run(generate_matrix(300))
    request_time = time.perf_counter() - start
    print("Request completed in {0:.0f}s for matrix 300 * 300".format(request_time))
