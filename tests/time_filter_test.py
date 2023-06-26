import pytest
from datetime import datetime

from traveltimepy import PublicTransport


@pytest.mark.asyncio
def test_departures(sdk, locations):
    results = sdk.time_filter_async(
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
def test_arrivals(sdk, locations):
    results = sdk.time_filter_async(
        locations=locations,
        search_ids={
            "London center": ["Hyde Park", "ZSL London Zoo"],
            "ZSL London Zoo": ["Hyde Park", "London center"],
        },
        transportation=PublicTransport(),
        departure_time=datetime.now(),
    )
    assert len(results) == 2
