import pytest
from datetime import datetime

from traveltimepy.dto import Location, Coordinates, LocationId
from traveltimepy.transportation import PublicTransport
from tests.fixture import sdk


@pytest.fixture
def locations():
    return [
        Location(id='London center', coords=Coordinates(lat=51.508930, lng=-0.131387)),
        Location(id='Hyde Park', coords=Coordinates(lat=51.508824, lng=-0.167093)),
        Location(id='ZSL London Zoo', coords=Coordinates(lat=51.536067, lng=-0.153596))
    ]


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

