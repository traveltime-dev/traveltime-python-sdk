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


class RoutesTest(unittest.TestCase):

    @mock.patch('requests.post', side_effect=mocked_requests)
    def test_routes(self, mock_post):
        sdk = TravelTimeSdk('appId', 'apiKey')
        locations = [
            Location(id='London center', coords=Coordinates(lat=51.508930, lng=-0.131387)),
            Location(id='Hyde Park', coords=Coordinates(lat=51.508824, lng=-0.167093)),
            Location(id='ZSL London Zoo', coords=Coordinates(lat=51.536067, lng=-0.153596))
        ]

        departure_search = DepartureSearch(
            id='departure search example',
            arrival_location_ids=['Hyde Park', 'ZSL London Zoo'],
            departure_location_id='London center',
            departure_time=datetime(2022, 11, 24, 12, 0, 0),
            transportation=PublicTransport(type='bus'),
            properties=[Property.TRAVEL_TIME],
            full_range=FullRange(enabled=True, max_results=3, width=600)
        )

        arrival_search = ArrivalSearch(
            id='arrival search example',
            departure_location_ids=['Hyde Park', 'ZSL London Zoo'],
            arrival_location_id='London center',
            arrival_time=datetime(2022, 11, 24, 12, 0, 0),
            transportation=PublicTransport(type='bus'),
            properties=[Property.TRAVEL_TIME, Property.FARES, Property.ROUTE],
        )

        response = sdk.routes(locations, [departure_search], [arrival_search])
        expected_response = parse_raw_as(RoutesResponse, read_file("tests/resources/responses/routes.json"))
        self.assertEqual(response, expected_response)
