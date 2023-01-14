from traveltimepy.dto import Coordinates
from traveltimepy.dto.requests.time_filter_proto import ProtoTransportation, Country
from tests.fixture import proto_sdk


def test_proto(proto_sdk):
    response = proto_sdk.time_filter_proto(
        origin=Coordinates(lat=51.425709, lng=-0.122061),
        destinations=[
            Coordinates(lat=51.348605, lng=-0.314783),
            Coordinates(lat=51.337205, lng=-0.315793)
        ],
        transportation=ProtoTransportation.DRIVING,
        travel_time=7200,
        country=Country.UNITED_KINGDOM
    )
    assert len(response.travel_times) == 2
