from datetime import datetime

from traveltimepy import Coordinates, PublicTransport


def test_districts_departure(sdk):
    results = sdk.postcodes(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315)],
        departure_time=datetime.now(),
        transportation=PublicTransport()
    )
    assert len(results) > 0


def test_districts_arrival(sdk):
    results = sdk.postcodes(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315)],
        arrival_time=datetime.now(),
        transportation=PublicTransport()
    )
    assert len(results) > 0


def test_sectors_departure(sdk):
    results = sdk.postcodes(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315)],
        departure_time=datetime.now(),
        transportation=PublicTransport()
    )
    assert len(results) > 0


def test_sectors_arrival(sdk):
    results = sdk.postcodes(
        coordinates=[Coordinates(lat=51.507609, lng=-0.128315)],
        arrival_time=datetime.now(),
        transportation=PublicTransport()
    )
    assert len(results) > 0
