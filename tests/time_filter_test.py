import unittest
from datetime import datetime

from unittest import mock

from tests.utils import mocked_requests, read_file
from traveltime.dto import Location, Coordinates, Property, FullRange, SearchId, LocationId
from traveltime.dto.requests.time_filter_request import DepartureSearch, ArrivalSearch
from traveltime.dto.responses.time_filter_response import TimeFilterResponse
from traveltime.sdk import TravelTimeSdk
from traveltime.transportation import Bus
from traveltime.utils import from_json


class TimeFilterTest(unittest.TestCase):

    @mock.patch('requests.post', side_effect=mocked_requests)
    def test_time_filter(self, mock_post):
        sdk = TravelTimeSdk('appId', 'apiKey')
        locations = [
            Location('London center', Coordinates(51.508930, -0.131387)),
            Location('Hyde Park', Coordinates(51.508824, -0.167093)),
            Location('ZSL London Zoo', Coordinates(51.536067, -0.153596))
        ]

        departure_search = DepartureSearch(
            SearchId('forward search example'),
            [LocationId('Hyde Park'), LocationId('ZSL London Zoo')],
            LocationId('London center'),
            datetime(2022, 11, 24, 12, 0, 0),
            3600,
            Bus(),
            [Property.TRAVEL_TIME],
            FullRange(True, 3, 600)
        )

        arrival_search = ArrivalSearch(
            SearchId('backward search example'),
            [LocationId('Hyde Park'), LocationId('ZSL London Zoo')],
            LocationId('London center'),
            datetime(2022, 11, 24, 12, 0, 0),
            3800,
            Bus(),
            [Property.TRAVEL_TIME, Property.FARES, Property.ROUTE],
        )

        response = sdk.time_filter(locations, [departure_search], [arrival_search])
        expected_response = from_json(TimeFilterResponse, read_file("resources/responses/time_filter.json"))
        self.assertEqual(response, expected_response)
