import unittest
from unittest import mock

from pydantic.tools import parse_raw_as

from tests.utils import mocked_requests, read_file
from traveltimepy.dto import Location, Coordinates
from traveltimepy.dto.responses.supported_locations import SupportedLocationsResponse
from traveltimepy.sdk import TravelTimeSdk


class SupportedLocationsTest(unittest.TestCase):

    @mock.patch('requests.post', side_effect=mocked_requests)
    def test_supported_locations(self, mock_get):
        sdk = TravelTimeSdk('appId', 'apiKey')
        locations = [
            Location(id='Kaunas', coords=Coordinates(lat=54.900008, lng=23.957734)),
            Location(id='London', coords=Coordinates(lat=51.506756, lng=-0.12805)),
            Location(id='Bangkok', coords=Coordinates(lat=13.761866, lng=100.544818)),
            Location(id='Lisbon', coords=Coordinates(lat=38.721869, lng=-9.138549)),
        ]
        response = sdk.supported_locations(locations)
        supported_locations = read_file('tests/resources/responses/supported_locations.json')
        expected_response = parse_raw_as(SupportedLocationsResponse, supported_locations)
        self.assertEqual(response, expected_response)
