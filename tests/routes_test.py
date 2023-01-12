import unittest
from datetime import datetime

from unittest import mock

from pydantic.tools import parse_raw_as

from tests.utils import mocked_requests, read_file
from traveltimepy.dto import Location, Coordinates
from traveltimepy.dto.requests import FullRange, Property
from traveltimepy.dto.requests.routes import DepartureSearch, ArrivalSearch
from traveltimepy.dto.responses.routes import RoutesResponse
from traveltimepy.sdk import TravelTimeSdk
from traveltimepy.transportation import PublicTransport



import pytest
from datetime import datetime

from traveltimepy.dto import LocationId
from traveltimepy.transportation import PublicTransport
from tests.fixture import sdk, locations


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

