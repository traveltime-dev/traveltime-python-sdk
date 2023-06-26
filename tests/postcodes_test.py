import pytest
from datetime import datetime

from traveltimepy import Coordinates, PublicTransport


@pytest.mark.asyncio
def test_departures(sdk):
    results = sdk.postcodes_async(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315)],
        departure_time=datetime.now(),
        transportation=PublicTransport(),
    )
    assert len(results) > 0


@pytest.mark.asyncio
def test_arrivals(sdk):
    results = sdk.postcodes_async(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315)],
        arrival_time=datetime.now(),
        transportation=PublicTransport(),
    )
    assert len(results) > 0


@pytest.mark.asyncio
def test_districts_departure(sdk):
    results = sdk.postcodes_districts_async(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315)],
        departure_time=datetime.now(),
        transportation=PublicTransport(),
    )
    assert len(results) > 0


@pytest.mark.asyncio
def test_districts_arrival(sdk):
    results = sdk.postcodes_districts_async(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315)],
        arrival_time=datetime.now(),
        transportation=PublicTransport(),
    )
    assert len(results) > 0


@pytest.mark.asyncio
def test_sectors_departure(sdk):
    results = sdk.postcodes_sectors_async(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315)],
        departure_time=datetime.now(),
        transportation=PublicTransport(),
    )
    assert len(results) > 0


@pytest.mark.asyncio
def test_sectors_arrival(sdk):
    results = sdk.postcodes_sectors_async(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315)],
        arrival_time=datetime.now(),
        transportation=PublicTransport(),
    )
    assert len(results) > 0
