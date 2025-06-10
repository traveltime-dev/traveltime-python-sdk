import pytest

from traveltimepy import TransportationFast, Property
from traveltimepy.async_client import AsyncClient
from traveltimepy.dto.requests.time_filter_fast import (
    TimeFilterFastArrivalSearches,
    TimeFilterFastOneToMany,
    TimeFilterFastManyToOne,
)


@pytest.mark.asyncio
async def test_one_to_many(async_client: AsyncClient, locations):
    results = await async_client.time_filter_fast(
        locations=locations,
        arrival_searches=TimeFilterFastArrivalSearches(
            one_to_many=[
                TimeFilterFastOneToMany(
                    id="London center",
                    departure_location_id="London center",
                    arrival_location_ids=["Hyde Park", "ZSL London Zoo"],
                    transportation=TransportationFast.DRIVING,
                    travel_time=1800,
                    properties=[Property.TRAVEL_TIME],
                ),
                TimeFilterFastOneToMany(
                    id="ZSL London Zoo",
                    departure_location_id="ZSL London Zoo",
                    arrival_location_ids=["Hyde Park", "London center"],
                    transportation=TransportationFast.DRIVING,
                    travel_time=1800,
                    properties=[Property.TRAVEL_TIME],
                ),
            ],
            many_to_one=[],
        ),
    )

    assert len(results) > 0


@pytest.mark.asyncio
async def test_many_to_one(async_client: AsyncClient, locations):
    results = await async_client.time_filter_fast(
        locations=locations,
        arrival_searches=TimeFilterFastArrivalSearches(
            many_to_one=[
                TimeFilterFastManyToOne(
                    id="London center",
                    arrival_location_id="London center",
                    departure_location_ids=["Hyde Park", "ZSL London Zoo"],
                    transportation=TransportationFast.DRIVING,
                    travel_time=1800,
                    properties=[Property.TRAVEL_TIME],
                ),
                TimeFilterFastManyToOne(
                    id="ZSL London Zoo",
                    arrival_location_id="ZSL London Zoo",
                    departure_location_ids=["Hyde Park", "London center"],
                    transportation=TransportationFast.DRIVING,
                    travel_time=1800,
                    properties=[Property.TRAVEL_TIME],
                ),
            ],
            one_to_many=[],
        ),
    )

    assert len(results) > 0
