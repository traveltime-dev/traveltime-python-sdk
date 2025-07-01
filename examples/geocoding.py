#!/usr/bin/env python3
"""
London walking tour planner

Plan a walking tour of famous London landmarks. Geocode the locations
to get coordinates, then calculate total walking time including
30-minute stops at each location.
"""

import os
from datetime import datetime

from traveltimepy import Client
from traveltimepy.requests.common import Location, Coordinates, Property
from traveltimepy.requests.time_filter import TimeFilterDepartureSearch
from traveltimepy.requests.transportation import Walking


def main():
    app_id = os.environ.get("TRAVELTIME_APP_ID")
    api_key = os.environ.get("TRAVELTIME_API_KEY")

    if not app_id or not api_key:
        print(
            "Error: Please set TRAVELTIME_APP_ID and TRAVELTIME_API_KEY environment variables"
        )
        exit(1)

    # London landmarks for walking tour
    landmarks = [
        "Big Ben, London",
        "London Eye, London",
        "Tower Bridge, London",
        "Westminster Abbey, London",
        "Buckingham Palace, London",
    ]

    with Client(app_id, api_key) as client:

        print("London Walking Tour Planner")
        print("Geocoding landmarks...")

        # Geocode all landmarks to get coordinates
        locations = []
        for i, landmark in enumerate(landmarks):
            result = client.geocoding(query=landmark, limit=1)
            if result.features:
                coords = result.features[0].geometry.coordinates
                location = Location(
                    id=f"landmark_{i}", coords=Coordinates(lat=coords[1], lng=coords[0])
                )
                locations.append(location)
                print(f"{landmark}: {coords[1]:.4f}, {coords[0]:.4f}")
            else:
                print(f"{landmark}: Not found")

        if len(locations) < 2:
            print("Need at least 2 locations for tour planning")
            return

        # Calculate walking times between consecutive landmarks
        print(f"\nCalculating walking times between {len(locations)} landmarks...")

        departure_time = datetime.now().replace(
            hour=10, minute=0, second=0, microsecond=0
        )
        total_walking_time = 0

        for i in range(len(locations) - 1):
            current = locations[i]
            next_location = locations[i + 1]

            # Calculate walking time from current to next landmark
            response = client.time_filter(
                locations=[current, next_location],
                departure_searches=[
                    TimeFilterDepartureSearch(
                        id=f"walk_{i}",
                        departure_location_id=current.id,
                        arrival_location_ids=[next_location.id],
                        departure_time=departure_time,
                        travel_time=3600,  # Max 1 hour walking
                        transportation=Walking(),
                        properties=[Property.TRAVEL_TIME],
                    )
                ],
                arrival_searches=[],
            )

            if response.results and response.results[0].locations:
                walking_time = (
                    response.results[0].locations[0].properties[0].travel_time
                )
                walking_minutes = walking_time // 60
                total_walking_time += walking_time

                print(
                    f"  {landmarks[i]} → {landmarks[i + 1]}: {walking_minutes} min walk"
                )
            else:
                print(f"  {landmarks[i]} → {landmarks[i + 1]}: Route not found")

        # Calculate total tour time
        stop_time = 30 * len(locations)  # 30 min at each landmark
        total_walking_minutes = total_walking_time // 60
        total_tour_minutes = total_walking_minutes + stop_time

        print("\nTour Summary:")
        print(f"  Walking time: {total_walking_minutes} minutes")
        print(f"  Stop time: {stop_time} minutes (30 min × {len(locations)} landmarks)")
        print(
            f"  Total tour time: {total_tour_minutes} minutes ({total_tour_minutes // 60}h {total_tour_minutes % 60}m)"
        )


if __name__ == "__main__":
    main()
