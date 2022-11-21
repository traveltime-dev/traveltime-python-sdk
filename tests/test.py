import json
import unittest
from unittest import mock
from datetime import datetime
from unittest.mock import patch

from requests import Response

from tests.utils import mocked_requests, read_file
from traveltime import Coordinate, SearchId
from traveltime.requests import ArrivalSearch, DepartureSearch
from traveltime.sdk import TravelTimeSdk
from traveltime.transportation import Driving
from traveltime.utils import to_json


class TimeMapTest(unittest.TestCase):

    def mocked_requests_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        if args[0] == 'https://api.traveltimeapp.com/v4/map-info':
            json_data = read_file("resources/responses/map_info.json")
            return MockResponse(json_data, 200)
        elif args[0] == 'http://someotherurl.com/anothertest.json':
            return MockResponse({"key2": "value2"}, 200)
        else:
            return MockResponse(None, 404)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get(self, mock_get):
        sdk = TravelTimeSdk('4da26ce0', '1724661047021afd210e49c3e5d2b5b8')

        res = sdk.map_info()

        print(res)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_base(self, mock_get):
        sdk = TravelTimeSdk('4da26ce0', '1724661047021afd210e49c3e5d2b5b8')
        search = DepartureSearch(
            SearchId('Test'),
            Coordinate(51.507609,  -0.128315),
            datetime.now(),
            900,
            Driving()
        )

        response = Response()
        response.status_code = 200
        response._content = read_file("resources/responses/time_map.json")

        print(type(response.content))
        mock_get.return_value = response
        res = sdk.time_map(departure_searches=[search])

        print(res)
        self.assertTrue(len(res.results) != 0)

    def test_time_map(self):
        pass

    @staticmethod
    def __read_file(path):
        with open(path, 'r') as file:
            return file.read().replace('\n', '')




