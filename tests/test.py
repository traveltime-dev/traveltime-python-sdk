import unittest
from datetime import datetime

from traveltime import Coordinate, SearchId
from traveltime.requests import DepartureSearch
from traveltime.sdk import TravelTimeSdk
from traveltime.transportation import Driving


class TimeMapTest(unittest.TestCase):

    def test_base(self):
        sdk = TravelTimeSdk('appId', 'apiKey')
        search = DepartureSearch(
            SearchId('Test'),
            Coordinate(51.507609,  -0.128315),
            datetime.now(),
            900,
            Driving()
        )
        res = sdk.time_map(departure_searches=[search])
        self.assertTrue(len(res.results) != 0)
