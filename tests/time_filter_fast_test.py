import pytest

from traveltimepy import AsyncClient
from traveltimepy.client import Client
from traveltimepy.requests.common import Property, Snapping
from traveltimepy.requests.time_filter_fast import (
    TimeFilterFastArrivalSearches,
    TimeFilterFastOneToMany,
    TimeFilterFastManyToOne,
)
from traveltimepy.requests.transportation import (
    DrivingFerryFast,
    DrivingPublicTransportFast,
    PublicTransportFast,
    FastTrafficModel,
)


@pytest.mark.asyncio
async def test_one_to_many(async_client: AsyncClient, locations):
    response = await async_client.time_filter_fast(
        locations=locations,
        arrival_searches=TimeFilterFastArrivalSearches(
            one_to_many=[
                TimeFilterFastOneToMany(
                    id="London center",
                    departure_location_id="London center",
                    arrival_location_ids=["Hyde Park", "ZSL London Zoo"],
                    transportation=PublicTransportFast(),
                    travel_time=1800,
                    properties=[Property.TRAVEL_TIME],
                ),
                TimeFilterFastOneToMany(
                    id="ZSL London Zoo",
                    departure_location_id="ZSL London Zoo",
                    arrival_location_ids=["Hyde Park", "London center"],
                    transportation=PublicTransportFast(),
                    travel_time=1800,
                    properties=[Property.TRAVEL_TIME],
                ),
            ],
            many_to_one=[],
        ),
    )

    assert len(response.results) > 0


@pytest.mark.asyncio
async def test_many_to_one(async_client: AsyncClient, locations):
    response = await async_client.time_filter_fast(
        locations=locations,
        arrival_searches=TimeFilterFastArrivalSearches(
            many_to_one=[
                TimeFilterFastManyToOne(
                    id="London center",
                    arrival_location_id="London center",
                    departure_location_ids=["Hyde Park", "ZSL London Zoo"],
                    transportation=PublicTransportFast(),
                    travel_time=1800,
                    properties=[Property.TRAVEL_TIME],
                ),
                TimeFilterFastManyToOne(
                    id="ZSL London Zoo",
                    arrival_location_id="ZSL London Zoo",
                    departure_location_ids=["Hyde Park", "London center"],
                    transportation=PublicTransportFast(),
                    travel_time=1800,
                    properties=[Property.TRAVEL_TIME],
                ),
            ],
            one_to_many=[],
        ),
    )

    assert len(response.results) > 0


def test_one_to_many_sync(client: Client, locations):
    response = client.time_filter_fast(
        locations=locations,
        arrival_searches=TimeFilterFastArrivalSearches(
            one_to_many=[
                TimeFilterFastOneToMany(
                    id="London center",
                    departure_location_id="London center",
                    arrival_location_ids=["Hyde Park", "ZSL London Zoo"],
                    transportation=PublicTransportFast(),
                    travel_time=1800,
                    properties=[Property.TRAVEL_TIME],
                ),
                TimeFilterFastOneToMany(
                    id="ZSL London Zoo",
                    departure_location_id="ZSL London Zoo",
                    arrival_location_ids=["Hyde Park", "London center"],
                    transportation=PublicTransportFast(),
                    travel_time=1800,
                    properties=[Property.TRAVEL_TIME],
                ),
            ],
            many_to_one=[],
        ),
    )

    assert len(response.results) > 0


def test_many_to_one_sync(client: Client, locations):
    response = client.time_filter_fast(
        locations=locations,
        arrival_searches=TimeFilterFastArrivalSearches(
            many_to_one=[
                TimeFilterFastManyToOne(
                    id="London center",
                    arrival_location_id="London center",
                    departure_location_ids=["Hyde Park", "ZSL London Zoo"],
                    transportation=PublicTransportFast(),
                    travel_time=1800,
                    properties=[Property.TRAVEL_TIME],
                ),
                TimeFilterFastManyToOne(
                    id="ZSL London Zoo",
                    arrival_location_id="ZSL London Zoo",
                    departure_location_ids=["Hyde Park", "London center"],
                    transportation=PublicTransportFast(),
                    travel_time=1800,
                    properties=[Property.TRAVEL_TIME],
                ),
            ],
            one_to_many=[],
        ),
    )

    assert len(response.results) > 0


@pytest.mark.asyncio
async def test_one_to_many_with_traffic_model(async_client: AsyncClient, locations):
    response = await async_client.time_filter_fast(
        locations=locations,
        arrival_searches=TimeFilterFastArrivalSearches(
            one_to_many=[
                TimeFilterFastOneToMany(
                    id="London center",
                    departure_location_id="London center",
                    arrival_location_ids=["Hyde Park", "ZSL London Zoo"],
                    transportation=DrivingFerryFast(
                        traffic_model=FastTrafficModel.PEAK
                    ),
                    travel_time=1800,
                    properties=[Property.TRAVEL_TIME],
                ),
            ],
            many_to_one=[],
        ),
    )

    assert len(response.results) > 0


@pytest.mark.asyncio
async def test_many_to_one_with_traffic_model(async_client: AsyncClient, locations):
    response = await async_client.time_filter_fast(
        locations=locations,
        arrival_searches=TimeFilterFastArrivalSearches(
            many_to_one=[
                TimeFilterFastManyToOne(
                    id="London center",
                    arrival_location_id="London center",
                    departure_location_ids=["Hyde Park", "ZSL London Zoo"],
                    transportation=DrivingFerryFast(
                        traffic_model=FastTrafficModel.OFF_PEAK
                    ),
                    travel_time=1800,
                    properties=[Property.TRAVEL_TIME],
                ),
            ],
            one_to_many=[],
        ),
    )

    assert len(response.results) > 0


def test_one_to_many_with_traffic_model_sync(client: Client, locations):
    response = client.time_filter_fast(
        locations=locations,
        arrival_searches=TimeFilterFastArrivalSearches(
            one_to_many=[
                TimeFilterFastOneToMany(
                    id="London center",
                    departure_location_id="London center",
                    arrival_location_ids=["Hyde Park", "ZSL London Zoo"],
                    transportation=DrivingFerryFast(
                        traffic_model=FastTrafficModel.PEAK
                    ),
                    travel_time=1800,
                    properties=[Property.TRAVEL_TIME],
                ),
            ],
            many_to_one=[],
        ),
    )

    assert len(response.results) > 0


def test_many_to_one_with_traffic_model_sync(client: Client, locations):
    response = client.time_filter_fast(
        locations=locations,
        arrival_searches=TimeFilterFastArrivalSearches(
            many_to_one=[
                TimeFilterFastManyToOne(
                    id="London center",
                    arrival_location_id="London center",
                    departure_location_ids=["Hyde Park", "ZSL London Zoo"],
                    transportation=DrivingFerryFast(
                        traffic_model=FastTrafficModel.OFF_PEAK
                    ),
                    travel_time=1800,
                    properties=[Property.TRAVEL_TIME],
                ),
            ],
            one_to_many=[],
        ),
    )

    assert len(response.results) > 0


@pytest.mark.asyncio
async def test_many_to_one_with_snapping_threshold(
    async_client: AsyncClient, locations
):
    response = await async_client.time_filter_fast(
        locations=locations,
        arrival_searches=TimeFilterFastArrivalSearches(
            many_to_one=[
                TimeFilterFastManyToOne(
                    id="London center",
                    arrival_location_id="London center",
                    departure_location_ids=["Hyde Park", "ZSL London Zoo"],
                    transportation=PublicTransportFast(),
                    travel_time=1800,
                    properties=[Property.TRAVEL_TIME],
                    snapping=Snapping(threshold=500),
                ),
            ],
            one_to_many=[],
        ),
    )

    assert len(response.results) > 0


def test_one_to_many_with_snapping_threshold_sync(client: Client, locations):
    response = client.time_filter_fast(
        locations=locations,
        arrival_searches=TimeFilterFastArrivalSearches(
            one_to_many=[
                TimeFilterFastOneToMany(
                    id="London center",
                    departure_location_id="London center",
                    arrival_location_ids=["Hyde Park", "ZSL London Zoo"],
                    transportation=PublicTransportFast(),
                    travel_time=1800,
                    properties=[Property.TRAVEL_TIME],
                    snapping=Snapping(threshold=500),
                ),
            ],
            many_to_one=[],
        ),
    )

    assert len(response.results) > 0


def test_public_transport_walking_time_limits_reach_sync(client: Client, locations):
    def reached(transportation):
        response = client.time_filter_fast(
            locations=locations,
            arrival_searches=TimeFilterFastArrivalSearches(
                one_to_many=[
                    TimeFilterFastOneToMany(
                        id="id",
                        departure_location_id="London center",
                        arrival_location_ids=["Hyde Park", "ZSL London Zoo"],
                        transportation=transportation,
                        travel_time=1800,
                        properties=[Property.TRAVEL_TIME],
                    )
                ],
                many_to_one=[],
            ),
        )
        return {
            loc.id: loc.properties.travel_time for loc in response.results[0].locations
        }

    unrestricted = reached(PublicTransportFast())
    short_walk = reached(PublicTransportFast(walking_time=60))
    assert unrestricted
    assert short_walk != unrestricted


def test_driving_public_transport_with_params_sync(client: Client, locations):
    response = client.time_filter_fast(
        locations=locations,
        arrival_searches=TimeFilterFastArrivalSearches(
            one_to_many=[
                TimeFilterFastOneToMany(
                    id="id",
                    departure_location_id="London center",
                    arrival_location_ids=["Hyde Park", "ZSL London Zoo"],
                    transportation=DrivingPublicTransportFast(
                        walking_time=600, driving_time_to_station=900, parking_time=120
                    ),
                    travel_time=1800,
                    properties=[Property.TRAVEL_TIME],
                )
            ],
            many_to_one=[],
        ),
    )
    assert len(response.results) == 1
