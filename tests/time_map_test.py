import unittest
from unittest import mock
from datetime import datetime

from tests.utils import mocked_requests, read_file
from traveltime.dto import Coordinates, SearchId, Range
from traveltime.dto.requests.time_map_request import DepartureSearch, ArrivalSearch, Union, Intersection
from traveltime.dto.responses.time_map_response import TimeMapResponse
from traveltime.sdk import TravelTimeSdk
from traveltime.transportation import PublicTransport, Driving
from traveltime.utils import from_json


class TimeMapTest(unittest.TestCase):

    @mock.patch('requests.post', side_effect=mocked_requests)
    def test_time_map(self, mock_post):
        sdk = TravelTimeSdk('appId', 'apiKey')
        departure_search1 = DepartureSearch(
            SearchId('search_1'),
            Coordinates(51.507609, -0.128315),
            datetime(2022, 11, 24, 12, 0, 0),
            900,
            PublicTransport()
        )
        departure_search2 = DepartureSearch(
            SearchId('search_2'),
            Coordinates(51.507609, -0.128315),
            datetime(2022, 11, 24, 12, 0, 0),
            900,
            Driving()
        )
        arrival_search = ArrivalSearch(
            SearchId('search_3'),
            Coordinates(51.507609, -0.128315),
            datetime(2022, 11, 24, 12, 0, 0),
            900,
            PublicTransport(),
            Range(True, 3600)
        )
        union = Union(
            SearchId('search_4'),
            [SearchId('search_2'), SearchId('search_3')]
        )
        intersection = Intersection(
            SearchId('search_5'),
            [SearchId('search_2'), SearchId('search_3')]
        )
        response = sdk.time_map(
            [arrival_search],
            [departure_search1, departure_search2],
            [union],
            [intersection]
        )
        expected_response = from_json(TimeMapResponse, read_file("resources/responses/time_map.json"))
        self.assertEqual(response, expected_response)



