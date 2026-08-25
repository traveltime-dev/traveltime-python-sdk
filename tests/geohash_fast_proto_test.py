import pytest

from traveltimepy.requests.common import Coordinates
from traveltimepy.async_client import AsyncClient
from traveltimepy.client import Client
from traveltimepy.requests.time_filter_proto import (
    ProtoDrivingAndPublicTransportWithDetails,
    ProtoTransportation,
    ProtoCountry,
    ProtoPublicTransportWithDetails,
    RequestType,
)
from traveltimepy.requests.geohash_fast_proto import ProtoCellProperty


@pytest.mark.asyncio
async def test_one_to_many(async_client: AsyncClient):
    response = await async_client.geohash_fast_proto(
        origin_coordinate=Coordinates(lat=51.425709, lng=-0.122061),
        transportation=ProtoTransportation.DRIVING_FERRY,
        travel_time=900,
        request_type=RequestType.ONE_TO_MANY,
        country=ProtoCountry.UNITED_KINGDOM,
        resolution=6,
        properties=[ProtoCellProperty.MEAN],
    )
    assert len(response.ids) > 0
    assert len(response.mean_travel_times) == len(response.ids)


@pytest.mark.asyncio
async def test_many_to_one(async_client: AsyncClient):
    response = await async_client.geohash_fast_proto(
        origin_coordinate=Coordinates(lat=51.425709, lng=-0.122061),
        transportation=ProtoTransportation.DRIVING_FERRY,
        travel_time=900,
        request_type=RequestType.MANY_TO_ONE,
        country=ProtoCountry.UNITED_KINGDOM,
        resolution=6,
        properties=[ProtoCellProperty.MEAN],
    )
    assert len(response.ids) > 0
    assert len(response.mean_travel_times) == len(response.ids)


@pytest.mark.asyncio
async def test_all_properties(async_client: AsyncClient):
    response = await async_client.geohash_fast_proto(
        origin_coordinate=Coordinates(lat=51.425709, lng=-0.122061),
        transportation=ProtoTransportation.DRIVING_FERRY,
        travel_time=900,
        request_type=RequestType.ONE_TO_MANY,
        country=ProtoCountry.UNITED_KINGDOM,
        resolution=6,
        properties=[
            ProtoCellProperty.MIN,
            ProtoCellProperty.MAX,
            ProtoCellProperty.MEAN,
        ],
    )
    assert len(response.ids) > 0
    assert len(response.min_travel_times) == len(response.ids)
    assert len(response.max_travel_times) == len(response.ids)
    assert len(response.mean_travel_times) == len(response.ids)


@pytest.mark.asyncio
async def test_one_to_many_pt_with_params(async_client: AsyncClient):
    response = await async_client.geohash_fast_proto(
        origin_coordinate=Coordinates(lat=51.425709, lng=-0.122061),
        transportation=ProtoPublicTransportWithDetails(walking_time_to_station=900),
        travel_time=900,
        request_type=RequestType.ONE_TO_MANY,
        country=ProtoCountry.UNITED_KINGDOM,
        resolution=6,
        properties=[ProtoCellProperty.MEAN],
    )
    assert len(response.ids) > 0


@pytest.mark.asyncio
async def test_many_to_one_pt_with_params(async_client: AsyncClient):
    response = await async_client.geohash_fast_proto(
        origin_coordinate=Coordinates(lat=51.425709, lng=-0.122061),
        transportation=ProtoPublicTransportWithDetails(walking_time_to_station=900),
        travel_time=900,
        request_type=RequestType.MANY_TO_ONE,
        country=ProtoCountry.UNITED_KINGDOM,
        resolution=6,
        properties=[ProtoCellProperty.MEAN],
    )
    assert len(response.ids) > 0


@pytest.mark.asyncio
async def test_one_to_many_driving_and_pt_with_params(async_client: AsyncClient):
    response = await async_client.geohash_fast_proto(
        origin_coordinate=Coordinates(lat=51.425709, lng=-0.122061),
        transportation=ProtoDrivingAndPublicTransportWithDetails(
            walking_time_to_station=900, driving_time_to_station=900, parking_time=300
        ),
        travel_time=900,
        request_type=RequestType.ONE_TO_MANY,
        country=ProtoCountry.UNITED_KINGDOM,
        resolution=6,
        properties=[ProtoCellProperty.MEAN],
    )
    assert len(response.ids) > 0


@pytest.mark.asyncio
async def test_many_to_one_driving_and_pt_with_params(async_client: AsyncClient):
    response = await async_client.geohash_fast_proto(
        origin_coordinate=Coordinates(lat=51.425709, lng=-0.122061),
        transportation=ProtoDrivingAndPublicTransportWithDetails(
            walking_time_to_station=900, driving_time_to_station=900, parking_time=300
        ),
        travel_time=900,
        request_type=RequestType.MANY_TO_ONE,
        country=ProtoCountry.UNITED_KINGDOM,
        resolution=6,
        properties=[ProtoCellProperty.MEAN],
    )
    assert len(response.ids) > 0


def test_one_to_many_sync(client: Client):
    response = client.geohash_fast_proto(
        origin_coordinate=Coordinates(lat=51.425709, lng=-0.122061),
        transportation=ProtoTransportation.DRIVING_FERRY,
        travel_time=900,
        request_type=RequestType.ONE_TO_MANY,
        country=ProtoCountry.UNITED_KINGDOM,
        resolution=6,
        properties=[ProtoCellProperty.MEAN],
    )
    assert len(response.ids) > 0
    assert len(response.mean_travel_times) == len(response.ids)


def test_many_to_one_sync(client: Client):
    response = client.geohash_fast_proto(
        origin_coordinate=Coordinates(lat=51.425709, lng=-0.122061),
        transportation=ProtoTransportation.DRIVING_FERRY,
        travel_time=900,
        request_type=RequestType.MANY_TO_ONE,
        country=ProtoCountry.UNITED_KINGDOM,
        resolution=6,
        properties=[ProtoCellProperty.MEAN],
    )
    assert len(response.ids) > 0
    assert len(response.mean_travel_times) == len(response.ids)


def test_keep_water_bodies_sync(client: Client):
    response = client.geohash_fast_proto(
        origin_coordinate=Coordinates(lat=51.425709, lng=-0.122061),
        transportation=ProtoTransportation.DRIVING_FERRY,
        travel_time=900,
        request_type=RequestType.ONE_TO_MANY,
        country=ProtoCountry.UNITED_KINGDOM,
        resolution=6,
        properties=[ProtoCellProperty.MEAN],
        remove_water_bodies=False,
    )
    assert len(response.ids) > 0
