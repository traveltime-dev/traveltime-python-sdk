import pytest
from datetime import datetime

from traveltimepy.dto import Location, Coordinates, LocationId
from traveltimepy.transportation import PublicTransport
from tests.fixture import sdk, locations


def test_departures(sdk, locations):
    response = sdk.time_filter(
        locations=locations,
        searches={
            LocationId('London center'): [LocationId('Hyde Park'), LocationId('ZSL London Zoo')],
            LocationId('ZSL London Zoo'): [LocationId('Hyde Park'), LocationId('London center')],
        },
        transportation=PublicTransport(),
        departure_time=datetime.now()
    )
    assert len(response.results) == 2


def test_arrivals(sdk, locations):
    response = sdk.time_filter(
        locations=locations,
        searches={
            LocationId('London center'): [LocationId('Hyde Park'), LocationId('ZSL London Zoo')],
            LocationId('ZSL London Zoo'): [LocationId('Hyde Park'), LocationId('London center')],
        },
        transportation=PublicTransport(),
        departure_time=datetime.now()
    )
    assert len(response.results) == 2

