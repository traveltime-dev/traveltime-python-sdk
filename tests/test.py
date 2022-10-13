import unittest
from datetime import datetime

from traveltime import Coordinate, SearchId
from traveltime.requests import ArrivalSearch
from traveltime.transportation import Driving
from traveltime.utils import to_json


class BasicTest(unittest.TestCase):

    def test_upper(self):
        arrival_search = ArrivalSearch(
            SearchId('Test'),
            Coordinate(12.23123, 12.123123),
            datetime.now(),
            3200,
            Driving()
        )
        print(to_json(arrival_search))
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)