import unittest
from datetime import datetime

from unittest import mock

from pydantic.tools import parse_raw_as

from tests.utils import mocked_requests, read_file
from traveltimepy.dto import Location, Coordinates
from traveltimepy.dto.requests import FullRange, Property
from traveltimepy.dto.requests.time_filter import DepartureSearch, ArrivalSearch
from traveltimepy.dto.responses.time_filter import TimeFilterResponse
from traveltimepy.sdk import TravelTimeSdk
from traveltimepy.transportation import PublicTransport


class TimeFilterTest(unittest.TestCase):

    @mock.patch('requests.post', side_effect=mocked_requests)
    def test_time_filter(self, mock_post):
        sdk = TravelTimeSdk('appId', 'apiKey')
        locations = [
            Location(id='London center', coords=Coordinates(lat=51.508930, lng=-0.131387)),
            Location(id='Hyde Park', coords=Coordinates(lat=51.508824, lng=-0.167093)),
            Location(id='ZSL London Zoo', coords=Coordinates(lat=51.536067, lng=-0.153596))
        ]

        departure_search = DepartureSearch(
            id='forward search example',
            arrival_location_ids=['Hyde Park', 'ZSL London Zoo'],
            departure_location_id='London center',
            departure_time=datetime(2022, 11, 24, 12, 0, 0),
            travel_time=3600,
            transportation=PublicTransport(type='bus'),
            properties=[Property.TRAVEL_TIME],
            full_range=FullRange(enabled=True, max_results=3, width=600)
        )

        arrival_search = ArrivalSearch(
            id='backward search example',
            departure_location_ids=['Hyde Park', 'ZSL London Zoo'],
            arrival_location_id='London center',
            arrival_time=datetime(2022, 11, 24, 12, 0, 0),
            travel_time=3800,
            transportation=PublicTransport(type='bus'),
            properties=[Property.TRAVEL_TIME, Property.FARES, Property.ROUTE],
        )

        response = sdk.time_filter(locations, [departure_search], [arrival_search])
        expected_response = parse_raw_as(TimeFilterResponse, read_file('tests/resources/responses/time_filter.json'))
        self.assertEqual(response, expected_response)
