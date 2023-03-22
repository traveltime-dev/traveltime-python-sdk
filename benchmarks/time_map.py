import asyncio
import time
from datetime import datetime

from benchmarks.common import generate_coordinates
from traveltimepy import TravelTimeSdk, Driving


async def generate_isochrones(size: int):
    sdk = TravelTimeSdk("APP_ID", "API_KEY")
    coordinates = generate_coordinates(51.507609, -0.128315, 0.05, size)
    return await sdk.time_map_async(
        coordinates=coordinates, transportation=Driving(), arrival_time=datetime.now()
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
