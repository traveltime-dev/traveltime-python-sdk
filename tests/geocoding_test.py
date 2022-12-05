import unittest
from unittest import mock

from geojson_pydantic import FeatureCollection
from pydantic.tools import parse_raw_as

from tests.utils import mocked_requests, read_file
from traveltimepy.sdk import TravelTimeSdk


class GeocodingTest(unittest.TestCase):

    @mock.patch('requests.get', side_effect=mocked_requests)
    def test_geocoding_search(self, mock_get):
        sdk = TravelTimeSdk('appId', 'apiKey')

        response = sdk.geocoding(query='Parliament square', limit=30)
        expected_response = parse_raw_as(FeatureCollection, read_file('tests/resources/responses/geocoding.json'))
        self.assertEqual(response, expected_response)

    @mock.patch('requests.get', side_effect=mocked_requests)
    def test_geocoding_reverse(self, mock_get):
        sdk = TravelTimeSdk('appId', 'apiKey')

        response = sdk.geocoding_reverse(lat=51.507281, lng=-0.132120)
        expected_response = parse_raw_as(FeatureCollection, read_file('tests/resources/responses/geocoding.json'))
        self.assertEqual(response, expected_response)
