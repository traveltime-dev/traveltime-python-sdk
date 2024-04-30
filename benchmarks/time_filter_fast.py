import asyncio
import time

from benchmarks.common import generate_locations
from traveltimepy import TravelTimeSdk, Transportation


async def generate_matrix(size: int):
    sdk = TravelTimeSdk("APP_ID", "API_KEY")
    locations = generate_locations(51.507609, -0.128315, 0.05, "Location", size)
    location_ids = [location.id for location in locations]
    search_ids = [
        (location_id, list(filter(lambda cur_id: cur_id != location_id, location_ids)))
        for location_id in location_ids
    ]
    return await sdk.time_filter_fast_async(
        locations=locations,
        search_ids=dict(search_ids),
        transportation=Transportation(type="driving"),
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
