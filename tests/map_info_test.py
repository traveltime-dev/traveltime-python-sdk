import unittest
from unittest import mock

from tests.utils import mocked_requests, read_file
from traveltime.dto.responses.map_info_response import MapInfoResponse
from traveltime.sdk import TravelTimeSdk
from traveltime.utils import from_json


class MapInfoTest(unittest.TestCase):

    @mock.patch('requests.get', side_effect=mocked_requests)
    def test_map_info(self, mock_get):
        sdk = TravelTimeSdk('appId', 'apiKey')

        response = sdk.map_info()
        expected_response = from_json(MapInfoResponse, read_file("resources/responses/map_info.json"))
        self.assertEqual(response, expected_response)
