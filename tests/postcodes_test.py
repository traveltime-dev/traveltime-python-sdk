from datetime import datetime

from traveltimepy.dto import Coordinates
from traveltimepy.transportation import PublicTransport


def test_departures(sdk):
    response = sdk.postcodes(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315)],
        departure_time=datetime.now(),
        transportation=PublicTransport()
    )
    assert len(response.results) > 0


def test_arrivals(sdk):
    response = sdk.postcodes(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315)],
        arrival_time=datetime.now(),
        transportation=PublicTransport()
    )
    assert len(response.results) > 0
