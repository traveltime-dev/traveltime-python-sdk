import unittest
from unittest import mock

from tests.utils import mocked_requests, read_file
from datetime import datetime
from pydantic import parse_raw_as

from traveltimepy.dto import Coordinates
from traveltimepy.dto.requests import Range
from traveltimepy.dto.requests.time_map import DepartureSearch, ArrivalSearch, Union, Intersection
from traveltimepy.dto.responses.time_map import TimeMapResponse
from traveltimepy.sdk import TravelTimeSdk
from traveltimepy.transportation import PublicTransport, Driving


class TimeMapTest(unittest.TestCase):

    @mock.patch('requests.post', side_effect=mocked_requests)
    def test_time_map(self, mock_post):
        sdk = TravelTimeSdk('appId', 'apiKey')
        departure_search1 = DepartureSearch(
            id='search_1',
            coords=Coordinates(lat=51.507609, lng=-0.128315),
            departure_time=datetime(2022, 11, 24, 12, 0, 0),
            travel_time=900,
            transportation=PublicTransport()
        )
        departure_search2 = DepartureSearch(
            id='search_2',
            coords=Coordinates(lat=51.507609, lng=-0.128315),
            departure_time=datetime(2022, 11, 24, 12, 0, 0),
            travel_time=900,
            transportation=Driving()
        )
        arrival_search = ArrivalSearch(
            id='search_3',
            coords=Coordinates(lat=51.507609, lng=-0.128315),
            arrival_time=datetime(2022, 11, 24, 12, 0, 0),
            travel_time=900,
            transportation=PublicTransport(),
            range=Range(enabled=True, width=3600)
        )
        union = Union(
            id='search_4',
            search_ids=['search_2', 'search_3']
        )
        intersection = Intersection(
            id='search_5',
            search_ids=['search_2', 'search_3']
        )
        response = sdk.time_map(
            [arrival_search],
            [departure_search1, departure_search2],
            [union],
            [intersection]
        )
        expected_response = parse_raw_as(TimeMapResponse, read_file('tests/resources/responses/time_map.json'))
        self.assertEqual(response, expected_response)
