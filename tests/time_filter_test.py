import pytest
from datetime import datetime

from traveltimepy import PublicTransport, TravelTimeSdk


@pytest.mark.asyncio
async def test_departures(sdk: TravelTimeSdk, locations):
    results = await sdk.time_filter_async(
        locations=locations,
        search_ids={
            "London center": ["Hyde Park", "ZSL London Zoo"],
            "ZSL London Zoo": ["Hyde Park", "London center"],
        },
        transportation=PublicTransport(),
        departure_time=datetime.now(),
    )
    assert len(results) == 2


@pytest.mark.asyncio
async def test_arrivals(sdk: TravelTimeSdk, locations):
    results = await sdk.time_filter_async(
        locations=locations,
        search_ids={
            "London center": ["Hyde Park", "ZSL London Zoo"],
            "ZSL London Zoo": ["Hyde Park", "London center"],
        },
        transportation=PublicTransport(),
        departure_time=datetime.now(),
    )
    assert len(results) == 2
