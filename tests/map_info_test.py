import unittest
from unittest import mock

from pydantic.tools import parse_raw_as

from tests.utils import mocked_requests, read_file
from traveltimepy.dto.responses.map_info import MapInfoResponse
from traveltimepy.sdk import TravelTimeSdk


class MapInfoTest(unittest.TestCase):

    @mock.patch('requests.get', side_effect=mocked_requests)
    def test_map_info(self, mock_get):
        sdk = TravelTimeSdk('appId', 'apiKey')

        response = sdk.map_info()
        expected_response = parse_raw_as(MapInfoResponse, read_file('tests/resources/responses/map_info.json'))
        self.assertEqual(response, expected_response)
