#!/usr/bin/env python3
"""Tourist route optimization analysis.

Calculate public transport travel times between random points in central London when
leaving at a specific time. The matrix helper splits the matrix into requests, retries
rate limits and failures, and returns travel times in input order.

Example output:
Travel Time Matrix (in seconds):
[0, 1204, 1856]
[1150, 0, 2134]
[1789, 2067, 0]

Unreachable destinations show None.
"""

import os
import random
from datetime import datetime
from typing import List

from traveltimepy.client import Client
from traveltimepy.requests.common import Coordinates
from traveltimepy.requests.transportation import PublicTransport


def generate_points(
    lat: float, lng: float, radius: float, amount: int
) -> List[Coordinates]:
    """Generate random points within `radius` degrees of a center point."""
    return [
        Coordinates(
            lat=random.uniform(lat - radius, lat + radius),
            lng=random.uniform(lng - radius, lng + radius),
        )
        for _ in range(amount)
    ]


def main():
    app_id = os.environ.get("TRAVELTIME_APP_ID")
    api_key = os.environ.get("TRAVELTIME_API_KEY")

    if not app_id or not api_key:
        print(
            "Error: Please set TRAVELTIME_APP_ID and TRAVELTIME_API_KEY environment variables"
        )
        exit(1)

    points = generate_points(lat=51.507609, lng=-0.128315, radius=0.05, amount=3)

    with Client(app_id, api_key) as client:
        matrix = client.time_filter_matrix(
            origins=points,
            destinations=points,
            transportation=PublicTransport(),
            travel_time=7200,
            departure_time=datetime.now(),
        )

    print("Travel Time Matrix (in seconds):")
    for row in matrix.travel_times:
        print(row)

    for failure in matrix.failures:
        print(f"Not computed: origins {failure.origins}, error: {failure.error}")


if __name__ == "__main__":
    main()
