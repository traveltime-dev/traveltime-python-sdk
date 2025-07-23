#!/usr/bin/env python3
"""
Fast tourist route optimization analysis

Calculate travel times between popular London attractions using the high-performance
time_filter_fast endpoint. This endpoint is optimized for large datasets with faster
response times but uses time periods instead of specific departure times. Creates a
symmetric matrix showing travel durations between all pairs of locations.

Example output:
Travel Time Matrix (in seconds):
[[   0 1204 1856]   # From London center to all locations
 [1150    0 2134]   # From Hyde Park to all locations  
 [1789 2067    0]]  # From ZSL London Zoo to all locations

The diagonal is always 0 (travel time from a location to itself).
Unreachable destinations would show -1.
"""

import os
from traveltimepy.client import Client
from traveltimepy.requests.common import Location, Coordinates, Property, ArrivalTimePeriod
from traveltimepy.requests.time_filter_fast import (
    TimeFilterFastArrivalSearches,
    TimeFilterFastOneToMany
)
from traveltimepy.requests.transportation import TransportationFast

import numpy as np


def define_locations():
    """Define the tourist attractions to analyze."""
    return [
        Location(id="London center", coords=Coordinates(lat=51.508930, lng=-0.131387)),
        Location(id="Hyde Park", coords=Coordinates(lat=51.508824, lng=-0.167093)),
        Location(id="ZSL London Zoo", coords=Coordinates(lat=51.536067, lng=-0.153596)),
    ]


def create_fast_searches(locations, properties=None):
    """Create fast one-to-many searches for each location.
    
    Args:
        locations: List of Location objects to search from
        properties: List of Property objects to request (defaults to [Property.TRAVEL_TIME])
    
    Returns:
        List of TimeFilterFastOneToMany objects
    """
    if properties is None:
        properties = [Property.TRAVEL_TIME]
        
    location_ids = [loc.id for loc in locations]
    return [
        TimeFilterFastOneToMany(
            id=origin.id,
            departure_location_id=origin.id,
            arrival_location_ids=location_ids,
            travel_time=7200,
            transportation=TransportationFast.PUBLIC_TRANSPORT,
            properties=properties,
            arrival_time_period=ArrivalTimePeriod.WEEKDAY_MORNING
        )
        for origin in locations
    ]


def build_matrix(results, locations, property_type=Property.TRAVEL_TIME):
    """Build a matrix from the API results for the specified property.
    
    Creates a symmetric matrix showing the requested property (travel time or distance)
    between all pairs of locations. The diagonal is filled with zeros since the
    travel time/distance from a location to itself is zero.
    
    Args:
        results: TimeFilterFastResponse object containing the API results
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
                    matrix[origin_idx, destination_idx] = loc.properties.travel_time
                elif property_type == Property.DISTANCE:
                    matrix[origin_idx, destination_idx] = loc.properties.distance
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

    locations = define_locations()
    matrix_property = Property.TRAVEL_TIME
    fast_searches = create_fast_searches(locations, [matrix_property])

    with Client(app_id, api_key) as client:
        results = client.time_filter_fast(
            locations=locations,
            arrival_searches=TimeFilterFastArrivalSearches(
                one_to_many=fast_searches,
                many_to_one=[]
            )
        )

        travel_time_matrix = build_matrix(results, locations, matrix_property)

        print("Travel Time Matrix (in seconds):")
        print(travel_time_matrix)


if __name__ == "__main__":
    main()