#!/usr/bin/env python3
"""
Public transport accessibility analysis

Check if essential services are reachable within 1 hour by public transport
from different residential areas.
"""

import asyncio
import os
from datetime import datetime

from traveltimepy import AsyncClient
from traveltimepy.requests.common import Coordinates, Location, Property
from traveltimepy.requests.time_filter import TimeFilterDepartureSearch
from traveltimepy.requests.transportation import PublicTransport


async def main():
    app_id = os.environ.get("TRAVELTIME_APP_ID")
    api_key = os.environ.get("TRAVELTIME_API_KEY")

    if not app_id or not api_key:
        print(
            "Error: Please set TRAVELTIME_APP_ID and TRAVELTIME_API_KEY environment variables"
        )
        exit(1)

    # Residential areas in London
    areas = [
        {"name": "Stratford", "coords": Coordinates(lat=51.5416, lng=-0.0022)},
        {"name": "Greenwich", "coords": Coordinates(lat=51.4769, lng=-0.0005)},
        {"name": "Croydon", "coords": Coordinates(lat=51.3762, lng=-0.0982)},
    ]

    # Essential services
    services = [
        {"name": "Hospital", "coords": Coordinates(lat=51.4685, lng=-0.0918)},
        {"name": "University", "coords": Coordinates(lat=51.4988, lng=-0.1749)},
        {"name": "Job Center", "coords": Coordinates(lat=51.5054, lng=-0.0235)},
    ]

    locations = []
    for i, area in enumerate(areas):
        locations.append(Location(id=f"area_{i}", coords=area["coords"]))
    for i, service in enumerate(services):
        locations.append(Location(id=f"service_{i}", coords=service["coords"]))

    departure_time = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)

    async with AsyncClient(app_id, api_key) as client:
        # Create concurrent searches for each area
        tasks = []
        for i, area in enumerate(areas):
            task = client.time_filter(
                locations=locations,
                departure_searches=[
                    TimeFilterDepartureSearch(
                        id=f"from_{area['name']}",
                        departure_location_id=f"area_{i}",
                        arrival_location_ids=[
                            f"service_{j}" for j in range(len(services))
                        ],
                        departure_time=departure_time,
                        travel_time=3600,  # 1 hour
                        transportation=PublicTransport(),
                        properties=[Property.TRAVEL_TIME],
                    )
                ],
                arrival_searches=[],
            )
            tasks.append((area["name"], task))

        # Execute all searches concurrently
        results = await asyncio.gather(*[task for _, task in tasks])

        total_reachable = 0
        for (area_name, _), result in zip(tasks, results):
            print(f"\nFrom {area_name}:")

            if result.results and result.results[0].locations:
                reachable = result.results[0].locations
                total_reachable += len(reachable)

                for location in reachable:
                    service_idx = int(location.id.split("_")[1])
                    service_name = services[service_idx]["name"]
                    minutes = location.properties[0].travel_time // 60
                    print(f"  {service_name}: {minutes} min")
            else:
                print("  No services reachable")

        print(f"\nTotal reachable: {total_reachable}/{len(areas) * len(services)}")


if __name__ == "__main__":
    asyncio.run(main())
