
from tests.fixture import sdk
from traveltimepy.dto import Location, Coordinates, LocationId
from traveltimepy.dto.requests.time_filter_fast import Transportation


def test_one_to_many(sdk):
    locations = [
        Location(id='London center', coords=Coordinates(lat=51.508930, lng=-0.131387)),
        Location(id='Hyde Park', coords=Coordinates(lat=51.508824, lng=-0.167093)),
        Location(id='ZSL London Zoo', coords=Coordinates(lat=51.536067, lng=-0.153596))
    ]

    response = sdk.time_filter_fast(
        locations=locations,
        searches={
            LocationId('London center'): [LocationId('Hyde Park'), LocationId('ZSL London Zoo')],
            LocationId('ZSL London Zoo'): [LocationId('Hyde Park'), LocationId('London center')],
        },
        transportation=Transportation(type='public_transport'),
    )

    assert len(response.results) > 0


def test_many_to_one(sdk):
    locations = [
        Location(id='London center', coords=Coordinates(lat=51.508930, lng=-0.131387)),
        Location(id='Hyde Park', coords=Coordinates(lat=51.508824, lng=-0.167093)),
        Location(id='ZSL London Zoo', coords=Coordinates(lat=51.536067, lng=-0.153596))
    ]

    response = sdk.time_filter_fast(
        locations=locations,
        searches={
            LocationId('London center'): [LocationId('Hyde Park'), LocationId('ZSL London Zoo')],
            LocationId('ZSL London Zoo'): [LocationId('Hyde Park'), LocationId('London center')],
        },
        transportation=Transportation(type='public_transport'),
        one_to_many=False
    )

    assert len(response.results) > 0
