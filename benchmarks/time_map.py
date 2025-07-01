import asyncio
import time
from datetime import datetime

from benchmarks.common import generate_locations
from traveltimepy.requests.transportation import Driving
from traveltimepy.async_client import AsyncClient
from traveltimepy.requests.time_map import TimeMapArrivalSearch


async def generate_isochrones(size: int):
    async with AsyncClient("APP_ID", "API_KEY") as async_client:
        locations = generate_locations(51.507609, -0.128315, 0.05, "isochrones", size)
        return await async_client.time_map(
            arrival_searches=[
                TimeMapArrivalSearch(
                    id=location.id,
                    coords=location.coords,
                    arrival_time=datetime.now(),
                    travel_time=3600,
                    transportation=Driving(),
                )
                for location in locations
            ],
            departure_searches=[],
            unions=[],
            intersections=[],
        )


if __name__ == "__main__":
    start = time.perf_counter()
    response = asyncio.run(generate_isochrones(50))
    request_time = time.perf_counter() - start
    print("Request completed in {0:.0f}s for 50 isochrones".format(request_time))

    start = time.perf_counter()
    response2 = asyncio.run(generate_isochrones(100))
    request_time = time.perf_counter() - start
    print("Request completed in {0:.0f}s for 100 isochrones".format(request_time))

    start = time.perf_counter()
    response3 = asyncio.run(generate_isochrones(300))
    request_time = time.perf_counter() - start
    print("Request completed in {0:.0f}s for 300 isochrones".format(request_time))
