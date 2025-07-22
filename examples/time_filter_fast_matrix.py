#!/usr/bin/env python3
"""
Fast office commute analysis

Calculate commute times using the high-performance time_filter_fast endpoint.
This endpoint is optimized for large datasets with faster response times
but uses time periods instead of specific departure times.
"""

import os

from traveltimepy import Client
from traveltimepy.requests.common import Coordinates, Location, Property, ArrivalTimePeriod
from traveltimepy.requests.time_filter_fast import (
    TimeFilterFastArrivalSearches,
    TimeFilterFastOneToMany
)
from traveltimepy.requests.transportation import TransportationFast


def main():
    app_id = os.environ.get("TRAVELTIME_APP_ID")
    api_key = os.environ.get("TRAVELTIME_API_KEY")

    if not app_id or not api_key:
        print("Error: Please set TRAVELTIME_APP_ID and TRAVELTIME_API_KEY environment variables")
        exit(1)

    residential_areas = [
        Location(id="stratford", coords=Coordinates(lat=51.5416, lng=-0.0022)),
        Location(id="greenwich", coords=Coordinates(lat=51.4769, lng=-0.0005)),
        Location(id="croydon", coords=Coordinates(lat=51.3762, lng=-0.0982)),
    ]
    
    office_locations = [
        Location(id="oxford_circus", coords=Coordinates(lat=51.5152, lng=-0.1416)),
        Location(id="london_bridge", coords=Coordinates(lat=51.5045, lng=-0.0865)),
        Location(id="canary_wharf", coords=Coordinates(lat=51.5054, lng=-0.0235)),
    ]

    print("Fast commute analysis for office relocation")
    print(f"Residential areas: {[area.id for area in residential_areas]}")
    print(f"Office options: {[office.id for office in office_locations]}")

    all_locations = residential_areas + office_locations

    one_to_many_searches = []
    for area in residential_areas:
        one_to_many_searches.append(
            TimeFilterFastOneToMany(
                id=f"fast_commute_from_{area.id}",
                departure_location_id=area.id,
                arrival_location_ids=[office.id for office in office_locations],
                travel_time=7200,  # 2 hours max commute
                transportation=TransportationFast.PUBLIC_TRANSPORT,
                properties=[Property.TRAVEL_TIME],
                arrival_time_period=ArrivalTimePeriod.WEEKDAY_MORNING
            )
        )

    with Client(app_id, api_key) as client:
        response = client.time_filter_fast(
            locations=all_locations,
            arrival_searches=TimeFilterFastArrivalSearches(
                one_to_many=one_to_many_searches,
                many_to_one=[]
            )
        )

        print("\nCommute Times (seconds):")
        print("-" * 60)
        
        offices = [office.id for office in office_locations]
        print(f"{'From':<15} {' '.join(f'{office:>12}' for office in offices)}")
        
        for i, result in enumerate(response.results):
            area_name = residential_areas[i].id
            
            reachable = {loc.id: loc.properties.travel_time for loc in result.locations}
            times = []
            for office in office_locations:
                if office.id in reachable:
                    seconds = reachable[office.id]
                    times.append(f"{seconds}")
                else:
                    times.append("-")
            
            print(f"{area_name:<15} {' '.join(f'{time:>12}' for time in times)}")


if __name__ == "__main__":
    main()