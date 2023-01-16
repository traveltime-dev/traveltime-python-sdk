from datetime import datetime

from traveltimepy import LocationId, PublicTransport


def test_departures(sdk, locations):
    results = sdk.routes(
        locations=locations,
        searches={
            LocationId('London center'): [LocationId('Hyde Park'), LocationId('ZSL London Zoo')],
            LocationId('ZSL London Zoo'): [LocationId('Hyde Park'), LocationId('London center')],
        },
        transportation=PublicTransport(),
        departure_time=datetime.now()
    )
    assert len(results) == 2


def test_arrivals(sdk, locations):
    results = sdk.routes(
        locations=locations,
        searches={
            LocationId('London center'): [LocationId('Hyde Park'), LocationId('ZSL London Zoo')],
            LocationId('ZSL London Zoo'): [LocationId('Hyde Park'), LocationId('London center')],
        },
        transportation=PublicTransport(),
        departure_time=datetime.now()
    )
    assert len(results) == 2
