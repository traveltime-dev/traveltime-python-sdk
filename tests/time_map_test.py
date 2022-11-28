import unittest
from unittest import mock

from tests.utils import mocked_requests, read_file
from traveltime.dto.requests.time_map import *
from pydantic import parse_raw_as
from traveltime.dto.responses.time_map import TimeMapResponse
from traveltime.sdk import TravelTimeSdk
from traveltime.transportation import PublicTransport, Driving


class TimeMapTest(unittest.TestCase):

    @mock.patch('requests.post', side_effect=mocked_requests)
    def test_time_map(self, mock_post):
        sdk = TravelTimeSdk('appId', 'apiKey')
        departure_search1 = DepartureSearch(
            id=SearchId('search_1'),
            coords=Coordinates(lat=51.507609, lng=-0.128315),
            departure_time=datetime(2022, 11, 24, 12, 0, 0),
            travel_time=900,
            transportation=PublicTransport()
        )
        departure_search2 = DepartureSearch(
            id=SearchId('search_2'),
            coords=Coordinates(lat=51.507609, lng=-0.128315),
            departure_time=datetime(2022, 11, 24, 12, 0, 0),
            travel_time=900,
            transportation=Driving()
        )
        arrival_search = ArrivalSearch(
            id=SearchId('search_3'),
            coords=Coordinates(lat=51.507609, lng=-0.128315),
            arrival_time=datetime(2022, 11, 24, 12, 0, 0),
            travel_time=900,
            transportation=PublicTransport(),
            range=Range(enabled=True, width=3600)
        )
        union = Union(
            id=SearchId('search_4'),
            search_ids=[SearchId('search_2'), SearchId('search_3')]
        )
        intersection = Intersection(
            id=SearchId('search_5'),
            search_ids=[SearchId('search_2'), SearchId('search_3')]
        )
        response = sdk.time_map(
            [arrival_search],
            [departure_search1, departure_search2],
            [union],
            [intersection]
        )
        expected_response = parse_raw_as(TimeMapResponse, read_file('resources/responses/time_map.json'))
        self.assertEqual(response, expected_response)

