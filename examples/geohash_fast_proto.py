#!/usr/bin/env python3
"""Geohash travel time analysis using Protocol Buffers API.

High-performance geohash-based travel time calculation.
"""

import asyncio
import os
from traveltimepy import AsyncClient
from traveltimepy.requests.common import Coordinates
from traveltimepy.requests.time_filter_proto import (
    ProtoTransportation,
    ProtoCountry,
    RequestType,
)
from traveltimepy.requests.geohash_fast_proto import ProtoCellProperty


async def main():
    app_id = os.environ.get("TRAVELTIME_APP_ID")
    api_key = os.environ.get("TRAVELTIME_API_KEY")

    if not app_id or not api_key:
        print(
            "Error: Please set TRAVELTIME_APP_ID and TRAVELTIME_API_KEY environment variables"
        )
        exit(1)

    origin = Coordinates(lat=51.4107, lng=-0.1554)

    async with AsyncClient(app_id, api_key) as client:
        response = await client.geohash_fast_proto(
            origin_coordinate=origin,
            transportation=ProtoTransportation.DRIVING_FERRY,
            travel_time=3600,  # 1 hour max
            request_type=RequestType.ONE_TO_MANY,
            country=ProtoCountry.UNITED_KINGDOM,
            resolution=4,
            properties=[
                ProtoCellProperty.MIN,
                ProtoCellProperty.MAX,
                ProtoCellProperty.MEAN,
            ],
        )

        print(f"Found {len(response.ids)} reachable geohash cells")
        for i, cell_id in enumerate(response.ids[:5]):
            print(
                f"  {cell_id}: min={response.min_travel_times[i]}s, "
                f"max={response.max_travel_times[i]}s, "
                f"mean={response.mean_travel_times[i]}s"
            )
        if len(response.ids) > 5:
            print(f"  ... and {len(response.ids) - 5} more")


if __name__ == "__main__":
    asyncio.run(main())
