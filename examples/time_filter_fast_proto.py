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
    app_id = os.environ.get("TRAVELTIME_APP_ID")
    api_key = os.environ.get("TRAVELTIME_API_KEY")

    if not app_id or not api_key:
        print(
            "Error: Please set TRAVELTIME_APP_ID and TRAVELTIME_API_KEY environment variables"
        )
        exit(1)

    origin = Coordinates(lat=51.4107, lng=-0.1554)

    # Generate 50 random shop locations
    shops = []
    for i in range(50):
        lat_offset = random.uniform(-0.005, 0.005)
        lng_offset = random.uniform(-0.005, 0.005)
        shops.append(
            Coordinates(lat=origin.lat + lat_offset, lng=origin.lng + lng_offset)
        )

    async with AsyncClient(app_id, api_key) as client:
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
