from datetime import datetime

import pytest

from traveltimepy import Property, Driving
from traveltimepy.async_client import AsyncClient
from traveltimepy.dto.requests.time_filter import (
    TimeFilterDepartureSearch,
    TimeFilterArrivalSearch,
)


@pytest.mark.asyncio
async def test_departures(async_client: AsyncClient, locations):
    results = await async_client.time_filter(
        locations=locations,
        departure_searches=[
            TimeFilterDepartureSearch(
                id="London center",
                departure_location_id="London center",
                arrival_location_ids=["Hyde Park", "ZSL London Zoo"],
                departure_time=datetime.now(),
                transportation=Driving(),
                travel_time=1800,
                properties=[Property.TRAVEL_TIME],
            ),
            TimeFilterDepartureSearch(
                id="ZSL London Zoo",
                departure_location_id="ZSL London Zoo",
                arrival_location_ids=["Hyde Park", "London center"],
                departure_time=datetime.now(),
                transportation=Driving(),
                travel_time=1800,
                properties=[Property.TRAVEL_TIME],
            ),
        ],
        arrival_searches=[],
    )
    assert len(results) == 2


@pytest.mark.asyncio
async def test_arrivals(async_client: AsyncClient, locations):
    results = await async_client.time_filter(
        locations=locations,
        arrival_searches=[
            TimeFilterArrivalSearch(
                id="London center",
                arrival_location_id="London center",
                departure_location_ids=["Hyde Park", "ZSL London Zoo"],
                arrival_time=datetime.now(),
                transportation=Driving(),
                travel_time=1800,
                properties=[Property.TRAVEL_TIME],
            ),
            TimeFilterArrivalSearch(
                id="ZSL London Zoo",
                arrival_location_id="ZSL London Zoo",
                departure_location_ids=["Hyde Park", "London center"],
                arrival_time=datetime.now(),
                transportation=Driving(),
                travel_time=1800,
                properties=[Property.TRAVEL_TIME],
            ),
        ],
        departure_searches=[],
    )
    assert len(results) == 2
