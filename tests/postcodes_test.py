from datetime import datetime

import pytest

from traveltimepy.async_client import AsyncClient
from traveltimepy.client import Client
from traveltimepy.requests.common import Coordinates
from traveltimepy.requests.postcodes import (
    PostcodeDepartureSearch,
    PostcodeArrivalSearch,
)
from traveltimepy.requests.postcodes_zones import (
    PostcodeFilterDepartureSearch,
    PostcodeFilterArrivalSearch,
)
from traveltimepy.requests.transportation import PublicTransport


@pytest.mark.asyncio
async def test_departures(async_client: AsyncClient):
    response = await async_client.postcodes(
        departure_searches=[
            PostcodeDepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                travel_time=900,
                departure_time=datetime.now(),
                transportation=PublicTransport(),
                properties=[],
            )
        ],
        arrival_searches=[],
    )
    assert len(response.results) > 0


@pytest.mark.asyncio
async def test_arrivals(async_client: AsyncClient):
    response = await async_client.postcodes(
        arrival_searches=[
            PostcodeArrivalSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                travel_time=900,
                arrival_time=datetime.now(),
                transportation=PublicTransport(),
                properties=[],
            )
        ],
        departure_searches=[],
    )
    assert len(response.results) > 0


@pytest.mark.asyncio
async def test_districts_departure(async_client: AsyncClient):
    response = await async_client.postcode_districts(
        departure_searches=[
            PostcodeFilterDepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                travel_time=900,
                departure_time=datetime.now(),
                transportation=PublicTransport(),
                properties=[],
            )
        ],
        arrival_searches=[],
    )
    assert len(response.results) > 0


@pytest.mark.asyncio
async def test_districts_arrival(async_client: AsyncClient):
    response = await async_client.postcode_districts(
        arrival_searches=[
            PostcodeFilterArrivalSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                travel_time=900,
                arrival_time=datetime.now(),
                transportation=PublicTransport(),
                properties=[],
            )
        ],
        departure_searches=[],
    )

    assert len(response.results) > 0


@pytest.mark.asyncio
async def test_sectors_departure(async_client: AsyncClient):
    response = await async_client.postcode_sectors(
        departure_searches=[
            PostcodeFilterDepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                travel_time=900,
                departure_time=datetime.now(),
                transportation=PublicTransport(),
                properties=[],
            )
        ],
        arrival_searches=[],
    )
    assert len(response.results) > 0


@pytest.mark.asyncio
async def test_sectors_arrival(async_client: AsyncClient):
    response = await async_client.postcode_sectors(
        arrival_searches=[
            PostcodeFilterArrivalSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                travel_time=900,
                arrival_time=datetime.now(),
                transportation=PublicTransport(),
                properties=[],
            )
        ],
        departure_searches=[],
    )

    assert len(response.results) > 0


def test_departures_sync(client: Client):
    response = client.postcodes(
        departure_searches=[
            PostcodeDepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                travel_time=900,
                departure_time=datetime.now(),
                transportation=PublicTransport(),
                properties=[],
            )
        ],
        arrival_searches=[],
    )
    assert len(response.results) > 0


def test_arrivals_sync(client: Client):
    response = client.postcodes(
        arrival_searches=[
            PostcodeArrivalSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                travel_time=900,
                arrival_time=datetime.now(),
                transportation=PublicTransport(),
                properties=[],
            )
        ],
        departure_searches=[],
    )
    assert len(response.results) > 0


def test_districts_departure_sync(client: Client):
    response = client.postcode_districts(
        departure_searches=[
            PostcodeFilterDepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                travel_time=900,
                departure_time=datetime.now(),
                transportation=PublicTransport(),
                properties=[],
            )
        ],
        arrival_searches=[],
    )
    assert len(response.results) > 0


def test_districts_arrival_sync(client: Client):
    response = client.postcode_districts(
        arrival_searches=[
            PostcodeFilterArrivalSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                travel_time=900,
                arrival_time=datetime.now(),
                transportation=PublicTransport(),
                properties=[],
            )
        ],
        departure_searches=[],
    )

    assert len(response.results) > 0


def test_sectors_departure_sync(client: Client):
    response = client.postcode_sectors(
        departure_searches=[
            PostcodeFilterDepartureSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                travel_time=900,
                departure_time=datetime.now(),
                transportation=PublicTransport(),
                properties=[],
            )
        ],
        arrival_searches=[],
    )
    assert len(response.results) > 0


def test_sectors_arrival_sync(client: Client):
    response = client.postcode_sectors(
        arrival_searches=[
            PostcodeFilterArrivalSearch(
                id="id",
                coords=Coordinates(lat=51.507609, lng=-0.128315),
                travel_time=900,
                arrival_time=datetime.now(),
                transportation=PublicTransport(),
                properties=[],
            )
        ],
        departure_searches=[],
    )

    assert len(response.results) > 0
