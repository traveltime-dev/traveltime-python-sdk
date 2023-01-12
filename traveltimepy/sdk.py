from datetime import datetime
from typing import List, Optional, Dict, TypeVar, Union, Tuple

from traveltime.transportation import PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain

from traveltimepy.dto.responses.time_filter_proto import TimeFilterProtoResponse
from traveltimepy.dto.requests.time_filter_proto import TimeFilterProtoRequest

from traveltimepy import AcceptType
from traveltimepy.dto import Location, Coordinates, LocationId
from traveltimepy.dto.requests import (
    time_map as time_map_package,
    time_filter as time_filter_package,
    time_filter_proto as time_filter_proto_package,
    routes as routes_package,
    postcodes as postcodes_package,
    zones,
    Rectangle, Property, FullRange
)
from traveltimepy.dto.requests.postcodes import PostcodesRequest
from traveltimepy.dto.requests.routes import RoutesRequest
from traveltimepy.dto.requests.supported_locations import SupportedLocationsRequest
from traveltimepy.dto.requests.time_filter import TimeFilterRequest
from traveltimepy.dto.requests.time_filter_fast import Transportation

from traveltimepy.dto.requests.time_map import Intersection, TimeMapRequest
from traveltimepy.dto.requests.zones import DistrictsRequest, SectorsRequest
from traveltimepy.dto.responses.map_info import MapInfoResponse
from traveltimepy.dto.responses.postcodes import PostcodesResponse
from traveltimepy.dto.responses.routes import RoutesResponse
from traveltimepy.dto.responses.supported_locations import SupportedLocationsResponse
from traveltimepy.dto.responses.time_filter import TimeFilterResponse
from traveltimepy.dto.responses.time_filter_fast import TimeFilterFastResponse
from traveltimepy.dto.responses.time_map import TimeMapResponse
from traveltimepy.dto.responses.zones import DistrictsResponse, SectorsResponse
from traveltimepy.errors import ApiError
from traveltimepy.itertools import join_opt
from traveltimepy.mapper import create_time_filter, create_time_filter_fast, create_postcodes
from traveltimepy.http import (
    send_get,
    send_get_async,
    send_post,
    send_post_async
)

from geojson_pydantic import FeatureCollection


class TravelTimeSdk:

    def __init__(self, app_id: str, api_key: str) -> None:
        self.__app_id = app_id
        self.__api_key = api_key

    async def time_filter_async(
        self,
        locations: List[Location],
        searches: Dict[LocationId, List[LocationId]],
        transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain],
        properties: Optional[List[Property]] = None,
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        travel_time: int = 3600,
        full_range: Optional[FullRange] = None
    ) -> TimeFilterResponse:
        return await send_post_async(
            TimeFilterResponse,
            'time-filter',
            self.__headers(AcceptType.JSON),
            create_time_filter(
                locations,
                searches,
                transportation,
                properties,
                departure_time,
                arrival_time,
                travel_time,
                full_range
            )
        )

    def time_filter(
        self,
        locations: List[Location],
        searches: Dict[LocationId, List[LocationId]],
        transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain],
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        properties: Optional[List[Property]] = None,
        travel_time: int = 3600,
        full_range: Optional[FullRange] = None
    ) -> TimeFilterResponse:
        res = send_post(
            TimeFilterResponse,
            'time-filter',
            self.__headers(AcceptType.JSON),
            create_time_filter(
                locations,
                searches,
                transportation,
                properties,
                departure_time,
                arrival_time,
                travel_time,
                full_range
            )
        )

        return res

    async def map_info_async(self) -> MapInfoResponse:
        return await send_get_async(MapInfoResponse, 'map-info', self.__headers(AcceptType.JSON))

    def map_info(self) -> MapInfoResponse:
        return send_get(MapInfoResponse, 'map-info', self.__headers(AcceptType.JSON))

    async def geocoding_async(
        self,
        query: str,
        limit: Optional[int] = None,
        within_countries: Optional[List[str]] = None,
        format_name: Optional[bool] = None,
        format_exclude_country: Optional[bool] = None,
        rectangle: Optional[Rectangle] = None
    ) -> FeatureCollection:
        return await send_get_async(
            FeatureCollection,
            'geocoding/search',
            self.__headers(AcceptType.JSON),
            self.__geocoding_params(
                query,
                limit,
                within_countries,
                format_name,
                format_exclude_country,
                rectangle
            )
        )

    def geocoding(
        self,
        query: str,
        limit: Optional[int] = None,
        within_countries: Optional[List[str]] = None,
        format_name: Optional[bool] = None,
        format_exclude_country: Optional[bool] = None,
        rectangle: Optional[Rectangle] = None
    ) -> FeatureCollection:
        return send_get(
            FeatureCollection,
            'geocoding/search',
            self.__headers(AcceptType.JSON),
            self.__geocoding_params(
                query,
                limit,
                within_countries,
                format_name,
                format_exclude_country,
                rectangle
            )
        )

    async def geocoding_reverse_async(
        self,
        lat: float,
        lng: float,
        within_countries: Optional[List[str]] = None
    ) -> FeatureCollection:
        return await send_get_async(
            FeatureCollection,
            'geocoding/reverse',
            self.__headers(AcceptType.JSON),
            self.__geocoding_reverse_params(lat, lng, within_countries)
        )

    def geocoding_reverse(
        self,
        lat: float,
        lng: float,
        within_countries: Optional[List[str]] = None
    ) -> FeatureCollection:
        return send_get(
            FeatureCollection,
            'geocoding/reverse',
            self.__headers(AcceptType.JSON),
            self.__geocoding_reverse_params(lat, lng, within_countries)
        )

    async def supported_locations_async(self, locations: List[Location]) -> SupportedLocationsResponse:
        return await send_post_async(
            SupportedLocationsResponse,
            'supported-locations',
            self.__headers(AcceptType.JSON),
            SupportedLocationsRequest(locations=locations)
        )

    def supported_locations(self, locations: List[Location]) -> SupportedLocationsResponse:
        return send_post(
            SupportedLocationsResponse,
            'supported-locations',
            self.__headers(AcceptType.JSON),
            SupportedLocationsRequest(locations=locations)
        )

    async def time_filter_fast_async(
        self,
        locations: List[Location],
        searches: Dict[LocationId, List[LocationId]],
        transportation: Transportation,
        travel_time: int = 3600,
        properties: Optional[List[Property]] = None,
        one_to_many: bool = False
    ) -> TimeFilterFastResponse:
        return await send_post_async(
            TimeFilterFastResponse,
            'time-filter/fast',
            self.__headers(AcceptType.JSON),
            create_time_filter_fast(
                locations,
                searches,
                transportation,
                travel_time,
                properties,
                one_to_many
            )
        )

    def time_filter_fast(
        self,
        locations: List[Location],
        searches: Dict[LocationId, List[LocationId]],
        transportation: Transportation,
        travel_time: int = 3600,
        properties: Optional[List[Property]] = None,
        one_to_many: bool = False
    ) -> TimeFilterFastResponse:
        return send_post(
            TimeFilterFastResponse,
            'time-filter/fast',
            self.__headers(AcceptType.JSON),
            create_time_filter_fast(
                locations,
                searches,
                transportation,
                travel_time,
                properties,
                one_to_many
            )
        )

    async def postcodes_async(
        self,
        coordinates: List[Coordinates],
        transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain],
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        travel_time: int = 3600,
        properties: Optional[List[Property]] = None,
        full_range: Optional[FullRange] = None
    ) -> PostcodesResponse:
        return await send_post_async(
            PostcodesResponse,
            'time-filter/postcodes',
            self.__headers(AcceptType.JSON),
            create_postcodes(
                coordinates,
                departure_time,
                arrival_time,
                transportation,
                travel_time,
                properties,
                full_range
            )
        )

    def postcodes(
        self,
        coordinates: List[Coordinates],
        transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain],
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        travel_time: int = 1800,
        properties: Optional[List[Property]] = None,
        full_range: Optional[FullRange] = None
    ) -> PostcodesResponse:
        return send_post(
            PostcodesResponse,
            'time-filter/postcodes',
            self.__headers(AcceptType.JSON),
            create_postcodes(
                coordinates,
                departure_time,
                arrival_time,
                transportation,
                travel_time,
                properties,
                full_range
            )
        )

    @staticmethod
    def __geocoding_reverse_params(
        lat: float,
        lng: float,
        within_countries: Optional[List[str]] = None
    ) -> Dict[str, str]:
        full_query = {
            'lat': lat,
            'lng': lng,
            'within.country': join_opt(within_countries, ',')
        }
        return {key: str(value) for (key, value) in full_query.items() if value is not None}

    @staticmethod
    def __geocoding_params(
        query: str,
        limit: Optional[int] = None,
        within_countries: Optional[List[str]] = None,
        format_name: Optional[bool] = None,
        format_exclude_country: Optional[bool] = None,
        rectangle: Optional[Rectangle] = None
    ) -> Dict[str, str]:
        full_query = {
            'query': query,
            'limit': limit,
            'within.country': join_opt(within_countries, ','),
            'format.name': format_name,
            'format.exclude.country': format_exclude_country,
            'bounds': rectangle.to_str() if rectangle is not None else rectangle
        }
        return {key: str(value) for (key, value) in full_query.items() if value is not None}

    def __headers(self, accept_type: AcceptType) -> Dict[str, str]:
        return {
            'X-Application-Id': self.__app_id,
            'X-Api-Key': self.__api_key,
            'User-Agent': 'Travel Time Python SDK',
            'Content-Type': 'application/json',
            'Accept': accept_type.value
        }

"""

    def time_filter_proto(self, one_to_many: time_filter_proto_package.OneToMany) -> TimeFilterProtoResponse:
        return send_proto_request(
            TimeFilterProtoRequest(one_to_many=one_to_many),
            self.__app_id,
            self.__api_key
        )

    def time_map(
        self,
        arrival_searches: List[time_map_package.ArrivalSearch],
        departure_searches: List[time_map_package.DepartureSearch],
        unions: List[Union] = [],
        intersections: List[Intersection] = []
    ) -> TimeMapResponse:
        return send_post_request(
            TimeMapResponse,
            'time-map',
            self.__headers(AcceptType.JSON),
            TimeMapRequest(
                departure_searches=departure_searches,
                arrival_searches=arrival_searches,
                unions=unions,
                intersections=intersections
            )
        )

    async def time_map_async(
        self,
        arrival_searches: List[time_map_package.ArrivalSearch],
        departure_searches: List[time_map_package.DepartureSearch],
        unions: List[Union] = [],
        intersections: List[Intersection] = []
    ) -> List[TimeMapResponse]:
        return await send_post_requests(
            TimeMapResponse,
            'time-map',
            self.__headers(AcceptType.JSON),
            self.split(
                TimeMapRequest(
                    departure_searches=departure_searches,
                    arrival_searches=arrival_searches,
                    unions=unions,
                    intersections=intersections
                )
            )
        )

    def split(self, request: TimeMapRequest) -> List[TimeMapRequest]:
        if len(request.arrival_searches) > 10 or len(request.departure_searches) > 10:
            res = list(
                itertools.zip_longest(
                    self.sliding(request.arrival_searches, 10),
                    self.sliding(request.departure_searches, 10),
                    fillvalue=[]
                )
            )
            requests = [TimeMapRequest(arrival_searches=arrival, departure_searches=departure, unions=[], intersections=[]) for
                        (arrival, departure) in res]
            return requests
        else:
            return [request]

    def postcodes(
        self,
        departure_searches: List[postcodes_package.DepartureSearch],
        arrival_searches: List[postcodes_package.ArrivalSearch]
    ) -> PostcodesResponse:
        return send_post_request(
            PostcodesResponse,
            'time-filter/postcodes',
            self.__headers(AcceptType.JSON),
            PostcodesRequest(
                departure_searches=departure_searches,
                arrival_searches=arrival_searches
            )
        )

    def districts(
        self,
        departure_searches: List[zones.DepartureSearch],
        arrival_searches: List[zones.ArrivalSearch]
    ) -> DistrictsResponse:
        return send_post_request(
            DistrictsResponse,
            'time-filter/postcode-districts',
            self.__headers(AcceptType.JSON),
            DistrictsRequest(
                departure_searches=departure_searches,
                arrival_searches=arrival_searches
            )
        )

    def sectors(
        self,
        departure_searches: List[zones.DepartureSearch],
        arrival_searches: List[zones.ArrivalSearch]
    ) -> SectorsResponse:
        return send_post_request(
            SectorsResponse,
            'time-filter/postcode-sectors',
            self.__headers(AcceptType.JSON),
            SectorsRequest(
                departure_searches=departure_searches,
                arrival_searches=arrival_searches
            )
        )

    def routes(
        self,
        locations: List[Location],
        departure_searches: List[routes_package.DepartureSearch],
        arrival_searches: List[routes_package.ArrivalSearch]
    ) -> RoutesResponse:
        return send_post_request(
            RoutesResponse,
            'routes',
            self.__headers(AcceptType.JSON),
            RoutesRequest(
                locations=locations,
                departure_searches=departure_searches,
                arrival_searches=arrival_searches
            )
        )

    async def routes_async(
        self,
        locations: List[Location],
        departure_searches: List[time_filter_package.DepartureSearch],
        arrival_searches: List[time_filter_package.ArrivalSearch]
    ) -> RoutesResponse:
        return await send_post_request_async(
            RoutesResponse,
            'routes',
            self.__headers(AcceptType.JSON),
            RoutesRequest(
                locations=locations,
                departure_searches=departure_searches,
                arrival_searches=arrival_searches
            )
        )
        
"""
