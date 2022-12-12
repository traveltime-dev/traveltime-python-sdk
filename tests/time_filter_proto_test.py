import os
import unittest

from traveltimepy.dto import Coordinates

from traveltimepy.dto.requests.time_filter_proto import OneToMany, Transportation, Country
from traveltimepy.sdk import TravelTimeSdk


class TimeFilterProtoTest(unittest.TestCase):

    def test_proto(self):
        sdk = TravelTimeSdk(os.environ['PROTO_APP_ID'], os.environ['PROTO_API_KEY'])
        one_to_many = OneToMany(
            origin_coordinates=Coordinates(lat=51.425709, lng=-0.122061),
            destination_coordinates=[
                Coordinates(lat=51.348605, lng=-0.314783),
                Coordinates(lat=51.337205, lng=-0.315793)
            ],
            transportation=Transportation.DRIVING,
            travel_time=7200,
            country=Country.UNITED_KINGDOM
        )

        response = sdk.time_filter_proto(one_to_many)
        self.assertEqual(len(response.travel_times), 2)
