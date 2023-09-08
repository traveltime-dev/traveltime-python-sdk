import pytest

from traveltimepy import Coordinates
from traveltimepy.dto.requests.time_filter_proto import (
    ProtoTransportation,
    ProtoCountry,
)


@pytest.mark.asyncio
async def test_one_to_many(proto_sdk):
    travel_times = await proto_sdk.time_filter_proto_async(
        origin=Coordinates(lat=51.425709, lng=-0.122061),
        destinations=[
            Coordinates(lat=51.348605, lng=-0.314783),
            Coordinates(lat=51.337205, lng=-0.315793),
        ],
        transportation=ProtoTransportation.DRIVING_FERRY,
        travel_time=7200,
        country=ProtoCountry.UNITED_KINGDOM,
    )
    assert len(travel_times) == 2


@pytest.mark.asyncio
async def test_many_to_one(proto_sdk):
    travel_times = await proto_sdk.time_filter_proto_async(
        origin=Coordinates(lat=51.425709, lng=-0.122061),
        destinations=[
            Coordinates(lat=51.348605, lng=-0.314783),
            Coordinates(lat=51.337205, lng=-0.315793),
        ],
        transportation=ProtoTransportation.DRIVING_FERRY,
        travel_time=7200,
        country=ProtoCountry.UNITED_KINGDOM,
        one_to_many=False
    )
    assert len(travel_times) == 2
