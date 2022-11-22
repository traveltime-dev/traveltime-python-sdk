import unittest
from unittest import mock
from datetime import datetime

from tests.utils import mocked_requests, read_file
from traveltime.dto import Coordinate, SearchId
from traveltime.dto.requests.time_map_request import DepartureSearch
from traveltime.dto.responses.map_info_response import MapInfoResponse
from traveltime.dto.responses.time_map_response import TimeMapResponse
from traveltime.sdk import TravelTimeSdk
from traveltime.transportation import Driving
from traveltime.utils import from_json


class TimeMapTest(unittest.TestCase):

    @mock.patch('requests.post', side_effect=mocked_requests)
    def test_time_map(self, mock_post):
        sdk = TravelTimeSdk('4da26ce0', '1724661047021afd210e49c3e5d2b5b8')
        search = DepartureSearch(
            SearchId('Test'),
            Coordinate(51.507609,  -0.128315),
            datetime.now(),
            900,
            Driving()
        )
        response = sdk.time_map(departure_searches=[search])
        expected_response = from_json(TimeMapResponse, read_file("resources/responses/time_map.json"))
        self.assertEqual(response, expected_response)



