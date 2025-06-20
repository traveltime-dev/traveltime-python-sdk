from datetime import datetime

import pytest

from traveltimepy.async_client import AsyncClient
from traveltimepy.client import Client
from traveltimepy.requests.common import Property
from traveltimepy.requests.time_filter import (
    TimeFilterDepartureSearch,
    TimeFilterArrivalSearch,
)
from traveltimepy.requests.transportation import PublicTransport


@pytest.mark.asyncio
async def test_departures(async_client: AsyncClient, locations):
    response = await async_client.time_filter(
        locations=locations,
        departure_searches=[
            TimeFilterDepartureSearch(
                id="London center",
                departure_location_id="London center",
                arrival_location_ids=["Hyde Park", "ZSL London Zoo"],
                departure_time=datetime.now(),
                transportation=PublicTransport(),
                travel_time=1800,
                properties=[Property.TRAVEL_TIME],
            ),
            TimeFilterDepartureSearch(
                id="ZSL London Zoo",
                departure_location_id="ZSL London Zoo",
                arrival_location_ids=["Hyde Park", "London center"],
                departure_time=datetime.now(),
                transportation=PublicTransport(),
                travel_time=1800,
                properties=[Property.TRAVEL_TIME],
            ),
        ],
        arrival_searches=[],
    )
    assert len(response.results) == 2


@pytest.mark.asyncio
async def test_arrivals(async_client: AsyncClient, locations):
    response = await async_client.time_filter(
        locations=locations,
        arrival_searches=[
            TimeFilterArrivalSearch(
                id="London center",
                arrival_location_id="London center",
                departure_location_ids=["Hyde Park", "ZSL London Zoo"],
                arrival_time=datetime.now(),
                transportation=PublicTransport(),
                travel_time=1800,
                properties=[Property.TRAVEL_TIME],
            ),
            TimeFilterArrivalSearch(
                id="ZSL London Zoo",
                arrival_location_id="ZSL London Zoo",
                departure_location_ids=["Hyde Park", "London center"],
                arrival_time=datetime.now(),
                transportation=PublicTransport(),
                travel_time=1800,
                properties=[Property.TRAVEL_TIME],
            ),
        ],
        departure_searches=[],
    )
    assert len(response.results) == 2


def test_departures_sync(client: Client, locations):
    response = client.time_filter(
        locations=locations,
        departure_searches=[
            TimeFilterDepartureSearch(
                id="London center",
                departure_location_id="London center",
                arrival_location_ids=["Hyde Park", "ZSL London Zoo"],
                departure_time=datetime.now(),
                transportation=PublicTransport(),
                travel_time=1800,
                properties=[Property.TRAVEL_TIME],
            ),
            TimeFilterDepartureSearch(
                id="ZSL London Zoo",
                departure_location_id="ZSL London Zoo",
                arrival_location_ids=["Hyde Park", "London center"],
                departure_time=datetime.now(),
                transportation=PublicTransport(),
                travel_time=1800,
                properties=[Property.TRAVEL_TIME],
            ),
        ],
        arrival_searches=[],
    )
    assert len(response.results) == 2


def test_arrivals_sync(client: Client, locations):
    response = client.time_filter(
        locations=locations,
        arrival_searches=[
            TimeFilterArrivalSearch(
                id="London center",
                arrival_location_id="London center",
                departure_location_ids=["Hyde Park", "ZSL London Zoo"],
                arrival_time=datetime.now(),
                transportation=PublicTransport(),
                travel_time=1800,
                properties=[Property.TRAVEL_TIME],
            ),
            TimeFilterArrivalSearch(
                id="ZSL London Zoo",
                arrival_location_id="ZSL London Zoo",
                departure_location_ids=["Hyde Park", "London center"],
                arrival_time=datetime.now(),
                transportation=PublicTransport(),
                travel_time=1800,
                properties=[Property.TRAVEL_TIME],
            ),
        ],
        departure_searches=[],
    )
    assert len(response.results) == 2
