import pytest

from traveltimepy import Coordinates
from traveltimepy.dto.common import PropertyProto
from traveltimepy.dto.requests.time_filter_proto import (
    DrivingAndPublicTransportWithDetails,
    ProtoTransportation,
    ProtoCountry,
    PublicTransportWithDetails,
)
from traveltimepy.sdk import TravelTimeSdk


@pytest.mark.asyncio
async def test_one_to_many(proto_sdk: TravelTimeSdk):
    results = await proto_sdk.time_filter_proto_async(
        origin=Coordinates(lat=51.425709, lng=-0.122061),
        destinations=[
            Coordinates(lat=51.348605, lng=-0.314783),
            Coordinates(lat=51.337205, lng=-0.315793),
        ],
        transportation=ProtoTransportation.DRIVING_FERRY,
        travel_time=7200,
        country=ProtoCountry.UNITED_KINGDOM,
    )
    assert len(results.travel_times) == 2 and len(results.distances) == 0


@pytest.mark.asyncio
async def test_many_to_one(proto_sdk: TravelTimeSdk):
    results = await proto_sdk.time_filter_proto_async(
        origin=Coordinates(lat=51.425709, lng=-0.122061),
        destinations=[
            Coordinates(lat=51.348605, lng=-0.314783),
            Coordinates(lat=51.337205, lng=-0.315793),
        ],
        transportation=ProtoTransportation.DRIVING_FERRY,
        travel_time=7200,
        country=ProtoCountry.UNITED_KINGDOM,
        one_to_many=False,
    )
    assert len(results.travel_times) == 2 and len(results.distances) == 0


@pytest.mark.asyncio
async def test_one_to_many_with_distances(proto_sdk: TravelTimeSdk):
    results = await proto_sdk.time_filter_proto_async(
        origin=Coordinates(lat=51.425709, lng=-0.122061),
        destinations=[
            Coordinates(lat=51.348605, lng=-0.314783),
            Coordinates(lat=51.337205, lng=-0.315793),
        ],
        transportation=ProtoTransportation.DRIVING_FERRY,
        travel_time=7200,
        country=ProtoCountry.UNITED_KINGDOM,
        properties=[PropertyProto.DISTANCE],
    )
    assert len(results.travel_times) == 2 and len(results.distances) == 2


@pytest.mark.asyncio
async def test_many_to_one_with_distances(proto_sdk: TravelTimeSdk):
    results = await proto_sdk.time_filter_proto_async(
        origin=Coordinates(lat=51.425709, lng=-0.122061),
        destinations=[
            Coordinates(lat=51.348605, lng=-0.314783),
            Coordinates(lat=51.337205, lng=-0.315793),
        ],
        transportation=ProtoTransportation.DRIVING_FERRY,
        travel_time=7200,
        country=ProtoCountry.UNITED_KINGDOM,
        one_to_many=False,
        properties=[PropertyProto.DISTANCE],
    )
    assert len(results.travel_times) == 2 and len(results.distances) == 2


async def test_one_to_many_pt_with_params(proto_sdk: TravelTimeSdk):
    results = await proto_sdk.time_filter_proto_async(
        origin=Coordinates(lat=51.425709, lng=-0.122061),
        destinations=[
            Coordinates(lat=51.348605, lng=-0.314783),
            Coordinates(lat=51.337205, lng=-0.315793),
        ],
        transportation=PublicTransportWithDetails(walking_time_to_station=900),
        travel_time=7200,
        country=ProtoCountry.UNITED_KINGDOM,
    )
    assert len(results.travel_times) == 2 and len(results.distances) == 0


@pytest.mark.asyncio
async def test_many_to_one_pt_with_params(proto_sdk: TravelTimeSdk):
    results = await proto_sdk.time_filter_proto_async(
        origin=Coordinates(lat=51.425709, lng=-0.122061),
        destinations=[
            Coordinates(lat=51.348605, lng=-0.314783),
            Coordinates(lat=51.337205, lng=-0.315793),
        ],
        transportation=PublicTransportWithDetails(walking_time_to_station=900),
        travel_time=7200,
        country=ProtoCountry.UNITED_KINGDOM,
        one_to_many=False,
    )
    assert len(results.travel_times) == 2 and len(results.distances) == 0


async def test_one_to_many_driving_and_pt_with_params(proto_sdk: TravelTimeSdk):
    results = await proto_sdk.time_filter_proto_async(
        origin=Coordinates(lat=51.425709, lng=-0.122061),
        destinations=[
            Coordinates(lat=51.348605, lng=-0.314783),
            Coordinates(lat=51.337205, lng=-0.315793),
        ],
        transportation=DrivingAndPublicTransportWithDetails(
            walking_time_to_station=900, driving_time_to_station=1800, parking_time=300
        ),
        travel_time=7200,
        country=ProtoCountry.UNITED_KINGDOM,
    )
    assert len(results.travel_times) == 2 and len(results.distances) == 0


@pytest.mark.asyncio
async def test_many_to_one_driving_and_pt_with_params(proto_sdk: TravelTimeSdk):
    results = await proto_sdk.time_filter_proto_async(
        origin=Coordinates(lat=51.425709, lng=-0.122061),
        destinations=[
            Coordinates(lat=51.348605, lng=-0.314783),
            Coordinates(lat=51.337205, lng=-0.315793),
        ],
        transportation=DrivingAndPublicTransportWithDetails(
            walking_time_to_station=900, driving_time_to_station=1800, parking_time=300
        ),
        travel_time=7200,
        country=ProtoCountry.UNITED_KINGDOM,
        one_to_many=False,
    )
    assert len(results.travel_times) == 2 and len(results.distances) == 0
