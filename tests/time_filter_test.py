from datetime import datetime

import pytest

from traveltimepy.async_client import AsyncClient
from traveltimepy.client import Client
from traveltimepy.requests.common import (
    Coordinates,
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
    DrivingPublicTransport,
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


def test_departures_driving_public_transport_sync(client: Client, locations):
    response = client.time_filter(
        locations=locations,
        departure_searches=[
            TimeFilterDepartureSearch(
                id="London center",
                departure_location_id="London center",
                arrival_location_ids=["Hyde Park", "ZSL London Zoo"],
                departure_time=datetime.now(),
                transportation=DrivingPublicTransport(
                    driving_time_to_station=600, parking_time=120, walking_time=300
                ),
                travel_time=1800,
                properties=[Property.TRAVEL_TIME],
            )
        ],
        arrival_searches=[],
    )
    assert len(response.results) == 1


def test_driving_public_transport_differs_from_driving_train_sync(client: Client):
    far_locations = [
        Location(id="London", coords=Coordinates(lat=51.507609, lng=-0.128315)),
        Location(id="Birmingham", coords=Coordinates(lat=52.4778, lng=-1.8990)),
        Location(id="Brighton", coords=Coordinates(lat=50.8292, lng=-0.1411)),
    ]

    def travel_times(transportation):
        response = client.time_filter(
            locations=far_locations,
            departure_searches=[
                TimeFilterDepartureSearch(
                    id="x",
                    departure_location_id="London",
                    arrival_location_ids=["Birmingham", "Brighton"],
                    departure_time=datetime.now(),
                    transportation=transportation,
                    travel_time=14400,
                    properties=[Property.TRAVEL_TIME],
                )
            ],
            arrival_searches=[],
        )
        return {
            loc.id: loc.properties[0].travel_time
            for loc in response.results[0].locations
        }

    assert travel_times(DrivingPublicTransport()) != travel_times(DrivingTrain())
