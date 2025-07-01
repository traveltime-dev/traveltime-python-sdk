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


@pytest.mark.asyncio
async def test_one_to_many(async_client: AsyncClient):
    response = await async_client.time_filter_fast_proto(
        origin_coordinate=Coordinates(lat=51.425709, lng=-0.122061),
        destination_coordinates=[
            Coordinates(lat=51.348605, lng=-0.314783),
            Coordinates(lat=51.337205, lng=-0.315793),
        ],
        transportation=ProtoTransportation.DRIVING_FERRY,
        travel_time=7200,
        request_type=RequestType.ONE_TO_MANY,
        country=ProtoCountry.UNITED_KINGDOM,
        with_distance=False,
    )
    assert len(response.travel_times) == 2 and len(response.distances) == 0


@pytest.mark.asyncio
async def test_many_to_one(async_client: AsyncClient):
    response = await async_client.time_filter_fast_proto(
        origin_coordinate=Coordinates(lat=51.425709, lng=-0.122061),
        destination_coordinates=[
            Coordinates(lat=51.348605, lng=-0.314783),
            Coordinates(lat=51.337205, lng=-0.315793),
        ],
        transportation=ProtoTransportation.DRIVING_FERRY,
        travel_time=7200,
        request_type=RequestType.MANY_TO_ONE,
        country=ProtoCountry.UNITED_KINGDOM,
        with_distance=False,
    )
    assert len(response.travel_times) == 2 and len(response.distances) == 0


@pytest.mark.asyncio
async def test_one_to_many_with_distances(async_client: AsyncClient):
    response = await async_client.time_filter_fast_proto(
        origin_coordinate=Coordinates(lat=51.425709, lng=-0.122061),
        destination_coordinates=[
            Coordinates(lat=51.348605, lng=-0.314783),
            Coordinates(lat=51.337205, lng=-0.315793),
        ],
        transportation=ProtoTransportation.DRIVING_FERRY,
        travel_time=7200,
        request_type=RequestType.ONE_TO_MANY,
        country=ProtoCountry.UNITED_KINGDOM,
        with_distance=True,
    )
    assert len(response.travel_times) == 2 and len(response.distances) == 2


@pytest.mark.asyncio
async def test_many_to_one_with_distances(async_client: AsyncClient):
    response = await async_client.time_filter_fast_proto(
        origin_coordinate=Coordinates(lat=51.425709, lng=-0.122061),
        destination_coordinates=[
            Coordinates(lat=51.348605, lng=-0.314783),
            Coordinates(lat=51.337205, lng=-0.315793),
        ],
        transportation=ProtoTransportation.DRIVING_FERRY,
        travel_time=7200,
        request_type=RequestType.MANY_TO_ONE,
        country=ProtoCountry.UNITED_KINGDOM,
        with_distance=True,
    )
    assert len(response.travel_times) == 2 and len(response.distances) == 2


@pytest.mark.asyncio
async def test_one_to_many_pt_with_params(async_client: AsyncClient):
    response = await async_client.time_filter_fast_proto(
        origin_coordinate=Coordinates(lat=51.425709, lng=-0.122061),
        destination_coordinates=[
            Coordinates(lat=51.348605, lng=-0.314783),
            Coordinates(lat=51.337205, lng=-0.315793),
        ],
        transportation=ProtoPublicTransportWithDetails(walking_time_to_station=900),
        travel_time=7200,
        request_type=RequestType.ONE_TO_MANY,
        country=ProtoCountry.UNITED_KINGDOM,
        with_distance=False,
    )
    assert len(response.travel_times) == 2 and len(response.distances) == 0


@pytest.mark.asyncio
async def test_many_to_one_pt_with_params(async_client: AsyncClient):
    response = await async_client.time_filter_fast_proto(
        origin_coordinate=Coordinates(lat=51.425709, lng=-0.122061),
        destination_coordinates=[
            Coordinates(lat=51.348605, lng=-0.314783),
            Coordinates(lat=51.337205, lng=-0.315793),
        ],
        transportation=ProtoPublicTransportWithDetails(walking_time_to_station=900),
        travel_time=7200,
        request_type=RequestType.MANY_TO_ONE,
        country=ProtoCountry.UNITED_KINGDOM,
        with_distance=False,
    )
    assert len(response.travel_times) == 2 and len(response.distances) == 0


@pytest.mark.asyncio
async def test_one_to_many_driving_and_pt_with_params(async_client: AsyncClient):
    response = await async_client.time_filter_fast_proto(
        origin_coordinate=Coordinates(lat=51.425709, lng=-0.122061),
        destination_coordinates=[
            Coordinates(lat=51.348605, lng=-0.314783),
            Coordinates(lat=51.337205, lng=-0.315793),
        ],
        transportation=ProtoDrivingAndPublicTransportWithDetails(
            walking_time_to_station=900, driving_time_to_station=1800, parking_time=300
        ),
        travel_time=7200,
        request_type=RequestType.ONE_TO_MANY,
        country=ProtoCountry.UNITED_KINGDOM,
        with_distance=False,
    )
    assert len(response.travel_times) == 2 and len(response.distances) == 0


@pytest.mark.asyncio
async def test_many_to_one_driving_and_pt_with_params(async_client: AsyncClient):
    response = await async_client.time_filter_fast_proto(
        origin_coordinate=Coordinates(lat=51.425709, lng=-0.122061),
        destination_coordinates=[
            Coordinates(lat=51.348605, lng=-0.314783),
            Coordinates(lat=51.337205, lng=-0.315793),
        ],
        transportation=ProtoDrivingAndPublicTransportWithDetails(
            walking_time_to_station=900, driving_time_to_station=1800, parking_time=300
        ),
        travel_time=7200,
        request_type=RequestType.MANY_TO_ONE,
        country=ProtoCountry.UNITED_KINGDOM,
        with_distance=False,
    )
    assert len(response.travel_times) == 2 and len(response.distances) == 0


def test_one_to_many_sync(client: Client):
    response = client.time_filter_fast_proto(
        origin_coordinate=Coordinates(lat=51.425709, lng=-0.122061),
        destination_coordinates=[
            Coordinates(lat=51.348605, lng=-0.314783),
            Coordinates(lat=51.337205, lng=-0.315793),
        ],
        transportation=ProtoTransportation.DRIVING_FERRY,
        travel_time=7200,
        request_type=RequestType.ONE_TO_MANY,
        country=ProtoCountry.UNITED_KINGDOM,
        with_distance=False,
    )
    assert len(response.travel_times) == 2 and len(response.distances) == 0


def test_many_to_one_sync(client: Client):
    response = client.time_filter_fast_proto(
        origin_coordinate=Coordinates(lat=51.425709, lng=-0.122061),
        destination_coordinates=[
            Coordinates(lat=51.348605, lng=-0.314783),
            Coordinates(lat=51.337205, lng=-0.315793),
        ],
        transportation=ProtoTransportation.DRIVING_FERRY,
        travel_time=7200,
        request_type=RequestType.MANY_TO_ONE,
        country=ProtoCountry.UNITED_KINGDOM,
        with_distance=False,
    )
    assert len(response.travel_times) == 2 and len(response.distances) == 0
