import asyncio
from datetime import datetime

from traveltimepy import Coordinates, Driving


def test_departures(sdk):
    results = asyncio.run(sdk.time_map_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            Coordinates(lat=51.517609, lng=-0.138315),
        ],
        departure_time=datetime.now(),
        travel_time=900,
        transportation=Driving(),
    ))
    assert len(results) == 2


def test_arrivals(sdk):
    results = asyncio.run(sdk.time_map_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            Coordinates(lat=51.517609, lng=-0.138315),
        ],
        arrival_time=datetime.now(),
        travel_time=900,
        transportation=Driving(),
    ))
    assert len(results) == 2


def test_union_departures(sdk):
    result = asyncio.run(sdk.union_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            Coordinates(lat=51.517609, lng=-0.138315),
        ],
        departure_time=datetime.now(),
        travel_time=900,
        transportation=Driving(),
    ))
    assert len(result.shapes) > 0


def test_intersection_arrivals(sdk):
    result = asyncio.run(sdk.intersection_async(
        coordinates=[
            Coordinates(lat=51.507609, lng=-0.128315),
            Coordinates(lat=51.517609, lng=-0.138315),
        ],
        arrival_time=datetime.now(),
        travel_time=900,
        transportation=Driving(),
    ))
    assert len(result.shapes) > 0
