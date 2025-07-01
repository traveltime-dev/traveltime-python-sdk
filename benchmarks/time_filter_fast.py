import asyncio
import time

from benchmarks.common import generate_locations
from traveltimepy.requests.common import Property
from traveltimepy.requests.transportation import TransportationFast
from traveltimepy.async_client import AsyncClient
from traveltimepy.requests.time_filter_fast import (
    TimeFilterFastArrivalSearches,
    TimeFilterFastOneToMany,
)


async def generate_matrix(size: int):
    async with AsyncClient("APP_ID", "API_KEY") as async_client:
        locations = generate_locations(51.507609, -0.128315, 0.05, "Location", size)
        location_ids = [location.id for location in locations]
        searches = [
            TimeFilterFastOneToMany(
                id=location_id,
                departure_location_id=location_id,
                arrival_location_ids=list(
                    filter(lambda cur_id: cur_id != location_id, location_ids)
                ),
                transportation=TransportationFast.DRIVING,
                travel_time=3600,
                properties=[Property.TRAVEL_TIME],
            )
            for location_id in location_ids
        ]

        return await async_client.time_filter_fast(
            locations=locations,
            arrival_searches=TimeFilterFastArrivalSearches(
                one_to_many=searches, many_to_one=[]
            ),
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
