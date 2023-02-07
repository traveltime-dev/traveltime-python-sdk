from datetime import datetime

from traveltimepy import PublicTransport


def test_departures(sdk, locations):
    results = sdk.routes(
        locations=locations,
        search_ids={
            'London center': ['Hyde Park', 'ZSL London Zoo'],
            'ZSL London Zoo': ['Hyde Park', 'London center'],
        },
        transportation=PublicTransport(),
        departure_time=datetime.now()
    )
    assert len(results) == 2


def test_arrivals(sdk, locations):
    results = sdk.routes(
        locations=locations,
        search_ids={
            'London center': ['Hyde Park', 'ZSL London Zoo'],
            'ZSL London Zoo': ['Hyde Park', 'London center'],
        },
        transportation=PublicTransport(),
        departure_time=datetime.now()
    )
    assert len(results) == 2
