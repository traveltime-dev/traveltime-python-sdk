from traveltimepy import LocationId
from traveltimepy.dto.requests.time_filter_fast import Transportation


def test_one_to_many(sdk, locations):
    results = sdk.time_filter_fast(
        locations=locations,
        searches={
            LocationId('London center'): [LocationId('Hyde Park'), LocationId('ZSL London Zoo')],
            LocationId('ZSL London Zoo'): [LocationId('Hyde Park'), LocationId('London center')],
        },
        transportation=Transportation(type='public_transport'),
    )

    assert len(results) > 0


def test_many_to_one(sdk, locations):
    results = sdk.time_filter_fast(
        locations=locations,
        searches={
            LocationId('London center'): [LocationId('Hyde Park'), LocationId('ZSL London Zoo')],
            LocationId('ZSL London Zoo'): [LocationId('Hyde Park'), LocationId('London center')],
        },
        transportation=Transportation(type='public_transport'),
        one_to_many=False
    )

    assert len(results) > 0
