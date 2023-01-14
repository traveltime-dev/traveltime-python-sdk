from datetime import datetime

from traveltimepy.dto import LocationId
from traveltimepy.transportation import PublicTransport


def test_departures(sdk, locations):
    response = sdk.routes(
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
    response = sdk.routes(
        locations=locations,
        searches={
            LocationId('London center'): [LocationId('Hyde Park'), LocationId('ZSL London Zoo')],
            LocationId('ZSL London Zoo'): [LocationId('Hyde Park'), LocationId('London center')],
        },
        transportation=PublicTransport(),
        departure_time=datetime.now()
    )
    assert len(response.results) == 2

