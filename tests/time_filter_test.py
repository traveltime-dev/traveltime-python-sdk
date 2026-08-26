from datetime import datetime

import pytest

from traveltimepy.async_client import AsyncClient
from traveltimepy.client import Client
from traveltimepy.requests.common import (
    GeohashCentroid,
    H3Centroid,
    Location,
    Property,
)
from traveltimepy.requests.time_filter import (
    TimeFilterDepartureSearch,
    TimeFilterArrivalSearch,
)
from traveltimepy.requests.transportation import (
    Driving,
    DrivingTrain,
    IncludeRoads,
    PublicTransport,
)


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


@pytest.mark.asyncio
async def test_departures_with_include_roads(async_client: AsyncClient, locations):
    response = await async_client.time_filter(
        locations=locations,
        departure_searches=[
            TimeFilterDepartureSearch(
                id="London center",
                departure_location_id="London center",
                arrival_location_ids=["Hyde Park", "ZSL London Zoo"],
                departure_time=datetime.now(),
                transportation=Driving(
                    include_roads=[IncludeRoads.TRACK, IncludeRoads.RESTRICTED]
                ),
                travel_time=1800,
                properties=[Property.TRAVEL_TIME],
            ),
        ],
        arrival_searches=[],
    )
    assert len(response.results) == 1


def test_departures_with_include_roads_sync(client: Client, locations):
    response = client.time_filter(
        locations=locations,
        departure_searches=[
            TimeFilterDepartureSearch(
                id="London center",
                departure_location_id="London center",
                arrival_location_ids=["Hyde Park", "ZSL London Zoo"],
                departure_time=datetime.now(),
                transportation=Driving(
                    include_roads=[IncludeRoads.TRACK, IncludeRoads.RESTRICTED]
                ),
                travel_time=1800,
                properties=[Property.TRAVEL_TIME],
            ),
        ],
        arrival_searches=[],
    )
    assert len(response.results) == 1


def test_departures_driving_train_with_boarding_time_sync(client: Client, locations):
    response = client.time_filter(
        locations=locations,
        departure_searches=[
            TimeFilterDepartureSearch(
                id="London center",
                departure_location_id="London center",
                arrival_location_ids=["Hyde Park", "ZSL London Zoo"],
                departure_time=datetime.now(),
                transportation=DrivingTrain(boarding_time=120),
                travel_time=1800,
                properties=[Property.TRAVEL_TIME],
            )
        ],
        arrival_searches=[],
    )
    assert len(response.results) == 1


@pytest.mark.asyncio
async def test_departures_with_centroid_locations(async_client: AsyncClient):
    response = await async_client.time_filter(
        locations=[
            Location(
                id="London center", coords=H3Centroid(h3_centroid="87195da49ffffff")
            ),
            Location(id="Hyde Park", coords=GeohashCentroid(geohash_centroid="gcpvj3")),
        ],
        departure_searches=[
            TimeFilterDepartureSearch(
                id="London center",
                departure_location_id="London center",
                arrival_location_ids=["Hyde Park"],
                departure_time=datetime.now(),
                transportation=PublicTransport(),
                travel_time=1800,
                properties=[Property.TRAVEL_TIME],
            )
        ],
        arrival_searches=[],
    )
    assert len(response.results) == 1


def test_departures_with_distance_breakdown_sync(client: Client, locations):
    response = client.time_filter(
        locations=locations,
        departure_searches=[
            TimeFilterDepartureSearch(
                id="London center",
                departure_location_id="London center",
                arrival_location_ids=["Hyde Park", "ZSL London Zoo"],
                departure_time=datetime.now(),
                transportation=Driving(),
                travel_time=1800,
                properties=[
                    Property.TRAVEL_TIME,
                    Property.DISTANCE,
                    Property.DISTANCE_BREAKDOWN,
                ],
            )
        ],
        arrival_searches=[],
    )

    assert len(response.results[0].locations) == 2
    for location in response.results[0].locations:
        properties = location.properties[0]
        assert properties.distance_breakdown
        total = sum(part.distance for part in properties.distance_breakdown)
        assert total == properties.distance
