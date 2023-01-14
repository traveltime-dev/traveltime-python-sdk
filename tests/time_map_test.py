from datetime import datetime

from traveltimepy.dto import Coordinates
from traveltimepy.transportation import Driving


def test_departures(sdk):
    response = sdk.time_map(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315), Coordinates(lat=51.507609, lng=-0.128315)],
        departure_time=datetime.now(),
        travel_time=900,
        transportation=Driving()
    )
    assert len(response.results) == 2


def test_arrivals(sdk):
    response = sdk.time_map(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315), Coordinates(lat=51.507609, lng=-0.128315)],
        arrival_time=datetime.now(),
        travel_time=900,
        transportation=Driving()
    )
    assert len(response.results) == 2
