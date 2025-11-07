#!/usr/bin/env python3
"""Tourist route optimization analysis.

Calculate travel times between popular London attractions to help tourists
plan efficient routes. Creates a symmetric matrix showing travel durations
between all pairs of locations for route optimization.

Example output:
Travel Time Matrix (in seconds):
[[   0 1204 1856]   # From London center to all locations
 [1150    0 2134]   # From Hyde Park to all locations
 [1789 2067    0]]  # From ZSL London Zoo to all locations

The diagonal is always 0 (travel time from a location to itself).
Unreachable destinations would show -1.
"""

import os
import random
from typing import List
from datetime import datetime
from traveltimepy.client import Client
from traveltimepy.requests.common import Location, Coordinates, Property
from traveltimepy.requests.time_filter import TimeFilterDepartureSearch
from traveltimepy.requests.transportation import PublicTransport

import numpy as np


def generate_locations(
    lat: float, lng: float, radius: float, amount: int
) -> List[Location]:
    """Generate a list of random locations around a given point.

    Args:
        lat: float value for latitude of the center point
        lng: float value for longitude of the center point
        radius: float value for the radius of the circle in which locations will be generated
        amount: int value for the amount of locations to generate

    Returns:
        List of randomly generated Location objects
    """

    def generate_float(value: float, radius: float) -> float:
        return random.uniform(value - radius, value + radius)

    return [
        Location(
            id="Location {}".format(i),
            coords=Coordinates(
                lat=generate_float(lat, radius), lng=generate_float(lng, radius)
            ),
        )
        for i in range(amount)
    ]


def define_locations():
    """Define custom tourist attractions to analyze."""
    return [
        Location(id="London center", coords=Coordinates(lat=51.508930, lng=-0.131387)),
        Location(id="Hyde Park", coords=Coordinates(lat=51.508824, lng=-0.167093)),
        Location(id="ZSL London Zoo", coords=Coordinates(lat=51.536067, lng=-0.153596)),
    ]


def create_departure_searches(locations, properties=None):
    """Create departure searches for each location.

    Args:
        locations: List of Location objects to search from
        properties: List of Property objects to request (defaults to [Property.TRAVEL_TIME])

    Returns:
        List of TimeFilterDepartureSearch objects
    """
    if properties is None:
        properties = [Property.TRAVEL_TIME]

    location_ids = [loc.id for loc in locations]
    return [
        TimeFilterDepartureSearch(
            id=origin.id,
            departure_location_id=origin.id,
            arrival_location_ids=location_ids,
            departure_time=datetime.now(),
            transportation=PublicTransport(),
            travel_time=7200,
            properties=properties,
        )
        for origin in locations
    ]


def build_matrix(results, locations, property_type=Property.TRAVEL_TIME):
    """Build a matrix from the API results for the specified property.

    Creates a symmetric matrix showing the requested property (travel time or distance)
    between all pairs of locations. The diagonal is filled with zeros since the
    travel time/distance from a location to itself is zero.

    Args:
        results: TimeFilterResponse object containing the API results
        locations: List of Location objects used in the search
        property_type: Property enum value specifying which property to extract:
            - Property.TRAVEL_TIME: Extract travel time in seconds (default)
            - Property.DISTANCE: Extract distance in meters

    Returns:
        numpy.ndarray: A symmetric matrix where matrix[i][j] represents the
                      requested property from location i to location j.
                      Unreachable destinations are marked with -1.
                      Diagonal elements are 0 (same location).

    Example:
        For 3 locations with travel times:
        [[   0, 1200, 1800],  # From location 0 to all locations
         [1150,    0, 2100],  # From location 1 to all locations
         [1750, 2050,    0]]  # From location 2 to all locations
    """
    # Create a list of all location IDs for easy index lookup later
    location_ids = [loc.id for loc in locations]
    n = len(location_ids)

    # Create a fast ID-to-Index mapping, as it will make searching a lot faster
    id_to_index = {loc_id: i for i, loc_id in enumerate(location_ids)}

    # Initialize matrix with -1 (unreachable) and set diagonal to 0
    matrix = np.full((n, n), -1, dtype=int)
    np.fill_diagonal(matrix, 0)

    for res in results.results:
        # Use the fast O(1) dictionary lookup
        origin_idx = id_to_index[res.search_id]

        for loc in res.locations:
            # Use the fast O(1) dictionary lookup
            destination_idx = id_to_index[loc.id]
            if loc.properties:
                # Extract the requested property value
                if property_type == Property.TRAVEL_TIME:
                    matrix[origin_idx, destination_idx] = loc.properties[0].travel_time
                elif property_type == Property.DISTANCE:
                    matrix[origin_idx, destination_idx] = loc.properties[0].distance
                else:
                    raise ValueError(f"Unsupported property_type: {property_type}")

    return matrix


def main():
    """Main function to calculate and display the travel time matrix."""
    app_id = os.environ.get("TRAVELTIME_APP_ID")
    api_key = os.environ.get("TRAVELTIME_API_KEY")

    if not app_id or not api_key:
        print(
            "Error: Please set TRAVELTIME_APP_ID and TRAVELTIME_API_KEY environment variables"
        )
        exit(1)

    """Generate a specified amount of random locations around a point."""
    MATRIX_SIZE = 3
    locations = generate_locations(
        lat=51.507609, lng=-0.128315, radius=0.05, amount=MATRIX_SIZE
    )

    # Or you can specify custom points of interests instead. Uncomment the line below if you wish to do so.
    # locations = define_locations()

    matrix_property = Property.TRAVEL_TIME
    departure_searches = create_departure_searches(locations, [matrix_property])

    with Client(app_id, api_key) as client:
        results = client.time_filter(
            locations=locations,
            departure_searches=departure_searches,
            arrival_searches=[],
        )

        travel_time_matrix = build_matrix(results, locations, matrix_property)

        print("Travel Time Matrix (in seconds):")
        print(travel_time_matrix)


if __name__ == "__main__":
    main()
