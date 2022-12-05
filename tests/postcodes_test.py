import unittest
from datetime import datetime
from unittest import mock

from pydantic import parse_raw_as

from tests.utils import mocked_requests, read_file
from traveltimepy.dto import Coordinates
from traveltimepy.dto.requests import Property
from traveltimepy.dto.requests.postcodes import DepartureSearch, ArrivalSearch
from traveltimepy.dto.responses.postcodes import PostcodesResponse
from traveltimepy.sdk import TravelTimeSdk
from traveltimepy.transportation import PublicTransport


class PostcodesTest(unittest.TestCase):

    @mock.patch('requests.post', side_effect=mocked_requests)
    def test_postcodes(self, mock_post):
        sdk = TravelTimeSdk('appId', 'apiKey')

        departure_search = DepartureSearch(
            id='public transport from Trafalgar Square',
            departure_time=datetime(2022, 11, 24, 12, 0, 0),
            travel_time=1800,
            coords=Coordinates(lat=51.507609, lng=-0.128315),
            transportation=PublicTransport(),
            properties=[Property.TRAVEL_TIME, Property.DISTANCE]
        )

        arrival_search = ArrivalSearch(
            id='public transport to Trafalgar Square',
            arrival_time=datetime(2022, 11, 24, 12, 0, 0),
            travel_time=1800,
            coords=Coordinates(lat=51.507609, lng=-0.128315),
            transportation=PublicTransport(),
            properties=[Property.TRAVEL_TIME, Property.DISTANCE]
        )

        response = sdk.postcodes([departure_search], [arrival_search])
        expected_response = parse_raw_as(PostcodesResponse, read_file('tests/resources/responses/postcodes.json'))
        self.assertEqual(response, expected_response)
