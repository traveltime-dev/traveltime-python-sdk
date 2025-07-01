#!/usr/bin/env python3
"""
Find closest shops by driving time using Protocol Buffers API

High-performance distance matrix calculation to find nearest stores.
"""

import asyncio
import os
import random
from traveltimepy import AsyncClient
from traveltimepy.requests.common import Coordinates
from traveltimepy.requests.time_filter_proto import (
    ProtoTransportation,
    ProtoCountry,
    RequestType,
)


async def main():
    api_key = os.environ.get("TRAVELTIME_API_KEY")
    api_secret = os.environ.get("TRAVELTIME_API_SECRET")

    if not api_key or not api_secret:
        print(
            "Error: Please set TRAVELTIME_API_KEY and TRAVELTIME_API_SECRET environment variables"
        )
        return

    origin = Coordinates(lat=51.4107, lng=-0.1554)

    # Generate 50 random shop locations
    shops = []
    for i in range(50):
        lat_offset = random.uniform(-0.005, 0.005)
        lng_offset = random.uniform(-0.005, 0.005)
        shops.append(
            Coordinates(lat=origin.lat + lat_offset, lng=origin.lng + lng_offset)
        )

    async with AsyncClient(api_key, api_secret) as client:
        # Find travel times using Proto API for maximum performance
        response = await client.time_filter_fast_proto(
            origin_coordinate=origin,
            destination_coordinates=shops,
            transportation=ProtoTransportation.DRIVING_FERRY,
            travel_time=3600,  # 1 hour max
            request_type=RequestType.ONE_TO_MANY,
            country=ProtoCountry.UNITED_KINGDOM,
            with_distance=False,
        )

        # Find 3 closest shops
        closest = []
        for i, travel_time in enumerate(response.travel_times):
            if travel_time > 0:
                closest.append((travel_time // 60, i + 1))

        closest.sort()

        print("3 closest shops:")
        for minutes, shop_id in closest[:3]:
            print(f"Shop {shop_id}: {minutes} min")


if __name__ == "__main__":
    asyncio.run(main())
