import unittest

from traveltimepy.dto import Coordinates

from traveltimepy.dto.requests.time_filter_proto import OneToMany, Transportation, Country
from traveltimepy.utils import to_proto_request


class TimeFilterProtoTest(unittest.TestCase):

    def test(self):
        one = OneToMany(
            Coordinates(lat=12.32, lng=13.32),
            [Coordinates(lat=12.32, lng=13.32)],
            Transportation.PUBLIC_TRANSPORT,
            Country.NETHERLANDS
        )

        to_proto_request(one)
