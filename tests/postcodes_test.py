import pytest
from datetime import datetime

from traveltimepy import Coordinates, PublicTransport, TravelTimeSdk


@pytest.mark.asyncio
async def test_departures(sdk: TravelTimeSdk):
    results = await sdk.postcodes_async(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315)],
        departure_time=datetime.now(),
        transportation=PublicTransport(),
    )
    assert len(results) > 0


@pytest.mark.asyncio
async def test_arrivals(sdk: TravelTimeSdk):
    results = await sdk.postcodes_async(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315)],
        arrival_time=datetime.now(),
        transportation=PublicTransport(),
    )
    assert len(results) > 0


@pytest.mark.asyncio
async def test_districts_departure(sdk: TravelTimeSdk):
    results = await sdk.postcodes_districts_async(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315)],
        departure_time=datetime.now(),
        transportation=PublicTransport(),
    )
    assert len(results) > 0


@pytest.mark.asyncio
async def test_districts_arrival(sdk: TravelTimeSdk):
    results = await sdk.postcodes_districts_async(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315)],
        arrival_time=datetime.now(),
        transportation=PublicTransport(),
    )
    assert len(results) > 0


@pytest.mark.asyncio
async def test_sectors_departure(sdk: TravelTimeSdk):
    results = await sdk.postcodes_sectors_async(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315)],
        departure_time=datetime.now(),
        transportation=PublicTransport(),
    )
    assert len(results) > 0


@pytest.mark.asyncio
async def test_sectors_arrival(sdk: TravelTimeSdk):
    results = await sdk.postcodes_sectors_async(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315)],
        arrival_time=datetime.now(),
        transportation=PublicTransport(),
    )
    assert len(results) > 0
