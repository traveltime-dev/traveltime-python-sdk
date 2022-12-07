import unittest

from unittest import mock

from pydantic.tools import parse_raw_as

from tests.utils import mocked_requests, read_file
from traveltimepy.dto import Location, Coordinates
from traveltimepy.dto.requests import Property
from traveltimepy.dto.requests.time_filter_fast import Transportation, ManyToOne, OneToMany
from traveltimepy.dto.responses.time_filter_fast import TimeFilterFastResponse
from traveltimepy.sdk import TravelTimeSdk


class TimeFilterFastTest(unittest.TestCase):

    @mock.patch('requests.post', side_effect=mocked_requests)
    def test_time_filter_fast(self, mock_post):
        sdk = TravelTimeSdk('appId', 'apiKey')
        locations = [
            Location(id='London center', coords=Coordinates(lat=51.508930, lng=-0.131387)),
            Location(id='Hyde Park', coords=Coordinates(lat=51.508824, lng=-0.167093)),
            Location(id='ZSL London Zoo', coords=Coordinates(lat=51.536067, lng=-0.153596))
        ]
        many_to_one = ManyToOne(
            id='many-to-one search example',
            departure_location_ids=['Hyde Park', 'ZSL London Zoo'],
            arrival_location_id='London center',
            transportation=Transportation(type='public_transport'),
            arrival_time_period='weekday_morning',
            travel_time=1900,
            properties=[Property.TRAVEL_TIME, Property.FARES]
        )
        one_to_many = OneToMany(
            id='one-to-many search example',
            arrival_location_ids=['Hyde Park', 'ZSL London Zoo'],
            departure_location_id='London center',
            transportation=Transportation(type='public_transport'),
            arrival_time_period='weekday_morning',
            travel_time=1900,
            properties=[Property.TRAVEL_TIME, Property.FARES]
        )

        response = sdk.time_filter_fast(locations, [many_to_one], [one_to_many])
        time_filter_response = read_file('tests/resources/responses/time_filter_fast.json')
        expected_response = parse_raw_as(TimeFilterFastResponse, time_filter_response)
        self.assertEqual(response, expected_response)
