import asyncio
from datetime import datetime

from traveltimepy import Coordinates, PublicTransport


def test_departures(sdk):
    results = asyncio.run(sdk.postcodes_async(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315)],
        departure_time=datetime.now(),
        transportation=PublicTransport(),
    ))
    assert len(results) > 0


def test_arrivals(sdk):
    results = asyncio.run(sdk.postcodes_async(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315)],
        arrival_time=datetime.now(),
        transportation=PublicTransport(),
    ))
    assert len(results) > 0


def test_districts_departure(sdk):
    results = asyncio.run(sdk.postcodes_districts_async(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315)],
        departure_time=datetime.now(),
        transportation=PublicTransport(),
    ))
    assert len(results) > 0


def test_districts_arrival(sdk):
    results = asyncio.run(sdk.postcodes_districts_async(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315)],
        arrival_time=datetime.now(),
        transportation=PublicTransport(),
    ))
    assert len(results) > 0


def test_sectors_departure(sdk):
    results = asyncio.run(sdk.postcodes_sectors_async(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315)],
        departure_time=datetime.now(),
        transportation=PublicTransport(),
    ))
    assert len(results) > 0


def test_sectors_arrival(sdk):
    results = asyncio.run(sdk.postcodes_sectors_async(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315)],
        arrival_time=datetime.now(),
        transportation=PublicTransport(),
    ))
    assert len(results) > 0
