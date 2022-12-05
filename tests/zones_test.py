import unittest
from datetime import datetime
from unittest import mock

from pydantic import parse_raw_as

from tests.utils import mocked_requests, read_file
from traveltimepy.dto import Coordinates
from traveltimepy.dto.requests.zones import DepartureSearch, ArrivalSearch, Property
from traveltimepy.dto.responses.zones import DistrictsResponse, SectorsResponse
from traveltimepy.sdk import TravelTimeSdk
from traveltimepy.transportation import PublicTransport


class ZonesTest(unittest.TestCase):
    @mock.patch('requests.post', side_effect=mocked_requests)
    def test_districts(self, mock_post):
        sdk = TravelTimeSdk('appId', 'apiKey')

        departure_search = DepartureSearch(
            id='public transport from Trafalgar Square',
            departure_time=datetime(2022, 11, 24, 12, 0, 0),
            travel_time=200,
            coords=Coordinates(lat=51.507609, lng=-0.128315),
            reachable_postcodes_threshold=0.1,
            transportation=PublicTransport(),
            properties=[Property.TRAVEL_TIME_ALL, Property.TRAVEL_TIME_REACHABLE]
        )

        arrival_search = ArrivalSearch(
            id='public transport to Trafalgar Square',
            arrival_time=datetime(2022, 11, 24, 12, 0, 0),
            travel_time=200,
            coords=Coordinates(lat=51.507609, lng=-0.128315),
            reachable_postcodes_threshold=0.1,
            transportation=PublicTransport(),
            properties=[Property.COVERAGE]
        )

        response = sdk.districts([departure_search], [arrival_search])
        expected_response = parse_raw_as(DistrictsResponse, read_file('tests/resources/responses/districts.json'))
        self.assertEqual(response, expected_response)

    @mock.patch('requests.post', side_effect=mocked_requests)
    def test_sectors(self, mock_post):
        sdk = TravelTimeSdk('appId', 'apiKey')

        departure_search = DepartureSearch(
            id='public transport from Trafalgar Square',
            departure_time=datetime(2022, 11, 24, 12, 0, 0),
            travel_time=200,
            coords=Coordinates(lat=51.507609, lng=-0.128315),
            reachable_postcodes_threshold=0.1,
            transportation=PublicTransport(),
            properties=[Property.TRAVEL_TIME_ALL, Property.TRAVEL_TIME_REACHABLE]
        )

        arrival_search = ArrivalSearch(
            id='public transport to Trafalgar Square',
            arrival_time=datetime(2022, 11, 24, 12, 0, 0),
            travel_time=200,
            coords=Coordinates(lat=51.507609, lng=-0.128315),
            reachable_postcodes_threshold=0.1,
            transportation=PublicTransport(),
            properties=[Property.COVERAGE]
        )

        response = sdk.sectors([departure_search], [arrival_search])
        expected_response = parse_raw_as(SectorsResponse, read_file('tests/resources/responses/sectors.json'))
        self.assertEqual(response, expected_response)
