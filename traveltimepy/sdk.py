from typing import List, Optional, Dict

from traveltimepy.dto.responses.time_filter_proto import TimeFilterProtoResponse
from traveltimepy.dto.requests.time_filter_proto import TimeFilterProtoRequest

from traveltimepy import AcceptType
from traveltimepy.dto import Location
from traveltimepy.dto.requests import (
    time_map as time_map_package,
    time_filter as time_filter_package,
    time_filter_proto as time_filter_proto_package,
    routes as routes_package,
    postcodes as postcodes_package,
    zones,
    Rectangle
)
from traveltimepy.dto.requests.postcodes import PostcodesRequest
from traveltimepy.dto.requests.routes import RoutesRequest
from traveltimepy.dto.requests.supported_locations import SupportedLocationsRequest
from traveltimepy.dto.requests.time_filter import TimeFilterRequest
from traveltimepy.dto.requests.time_filter_fast import ArrivalSearches, TimeFilterFastRequest, ManyToOne, OneToMany

from traveltimepy.dto.requests.time_map import Union, Intersection, TimeMapRequest
from traveltimepy.dto.requests.zones import DistrictsRequest, SectorsRequest
from traveltimepy.dto.responses.map_info import MapInfoResponse
from traveltimepy.dto.responses.postcodes import PostcodesResponse
from traveltimepy.dto.responses.routes import RoutesResponse
from traveltimepy.dto.responses.supported_locations import SupportedLocationsResponse
from traveltimepy.dto.responses.time_filter import TimeFilterResponse
from traveltimepy.dto.responses.time_filter_fast import TimeFilterFastResponse
from traveltimepy.dto.responses.time_map import TimeMapResponse
from traveltimepy.dto.responses.zones import DistrictsResponse, SectorsResponse
from traveltimepy.utils import (
    send_get_request,
    send_post_request,
    send_post_request_async,
    send_get_request_async,
    send_proto_request
)

from geojson_pydantic import FeatureCollection


class TravelTimeSdk:

    def __init__(self, app_id: str, api_key: str) -> None:
        self.__app_id = app_id
        self.__api_key = api_key

    def time_filter_proto(self, one_to_many: time_filter_proto_package.OneToMany) -> TimeFilterProtoResponse:
        return send_proto_request(
            TimeFilterProtoRequest(one_to_many=one_to_many),
            self.__app_id,
            self.__api_key
        )

    def map_info(self) -> MapInfoResponse:
        return send_get_request(MapInfoResponse, 'map-info', self.__headers(AcceptType.JSON))

    async def map_info_async(self) -> MapInfoResponse:
        return await send_get_request_async(MapInfoResponse, 'map-info', self.__headers(AcceptType.JSON))

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
    ) -> TimeMapResponse:
        return await send_post_request_async(
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

    def time_filter(
        self,
        locations: List[Location],
        departure_searches: List[time_filter_package.DepartureSearch],
        arrival_searches: List[time_filter_package.ArrivalSearch]
    ) -> TimeFilterResponse:
        return send_post_request(
            TimeFilterResponse,
            'time-filter',
            self.__headers(AcceptType.JSON),
            TimeFilterRequest(
                locations=locations,
                departure_searches=departure_searches,
                arrival_searches=arrival_searches
            )
        )

    async def time_filter_async(
        self,
        locations: List[Location],
        departure_searches: List[time_filter_package.DepartureSearch],
        arrival_searches: List[time_filter_package.ArrivalSearch]
    ) -> TimeFilterResponse:
        return await send_post_request_async(
            TimeFilterResponse,
            'time-filter',
            self.__headers(AcceptType.JSON),
            TimeFilterRequest(
                locations=locations,
                departure_searches=departure_searches,
                arrival_searches=arrival_searches
            )
        )

    def time_filter_fast(
        self,
        locations: List[Location],
        many_to_one: List[ManyToOne],
        one_to_many: List[OneToMany]
    ) -> TimeFilterFastResponse:
        return send_post_request(
            TimeFilterFastResponse,
            'time-filter/fast',
            self.__headers(AcceptType.JSON),
            TimeFilterFastRequest(
                locations=locations,
                arrival_searches=ArrivalSearches(many_to_one=many_to_one, one_to_many=one_to_many)
            )
        )

    async def time_filter_fast_async(
        self,
        locations: List[Location],
        many_to_one: List[ManyToOne],
        one_to_many: List[OneToMany]
    ) -> TimeFilterFastResponse:
        return await send_post_request_async(
            TimeFilterFastResponse,
            'time-filter/fast',
            self.__headers(AcceptType.JSON),
            TimeFilterFastRequest(
                locations=locations,
                arrival_searches=ArrivalSearches(many_to_one=many_to_one, one_to_many=one_to_many)
            )
        )

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

    def geocoding(
        self,
        query: str,
        limit: Optional[int] = None,
        within_countries: Optional[List[str]] = None,
        format_name: Optional[bool] = None,
        format_exclude_country: Optional[bool] = None,
        rectangle: Optional[Rectangle] = None
    ) -> FeatureCollection:
        full_query = {
            'query': query,
            'limit': limit,
            'within.country': self.__combine_countries(within_countries),
            'format.name': format_name,
            'format.exclude.country': format_exclude_country,
            'bounds': self.__bounds(rectangle)
        }
        params = {key: str(value) for (key, value) in full_query.items() if value is not None}
        return send_get_request(FeatureCollection, 'geocoding/search', self.__headers(AcceptType.JSON), params)

    def geocoding_reverse(
        self,
        lat: float,
        lng: float,
        within_countries: Optional[List[str]] = None
    ) -> FeatureCollection:
        full_query = {
            'lat': lat,
            'lng': lng,
            'within.country': self.__combine_countries(within_countries)
        }
        params = {key: str(value) for (key, value) in full_query.items() if value is not None}
        return send_get_request(FeatureCollection, 'geocoding/reverse', self.__headers(AcceptType.JSON), params)

    def supported_locations(self, locations: List[Location]) -> SupportedLocationsResponse:
        return send_post_request(
            SupportedLocationsResponse,
            'supported-locations',
            self.__headers(AcceptType.JSON),
            SupportedLocationsRequest(locations=locations)
        )

    @staticmethod
    def __bounds(rectangle: Optional[Rectangle]) -> Optional[str]:
        if rectangle is not None:
            return f'{rectangle.min_lat},{rectangle.min_lng},{rectangle.max_lat},{rectangle.max_lng}'
        else:
            return None

    @staticmethod
    def __combine_countries(within_countries: Optional[List[str]]) -> Optional[str]:
        return ','.join(within_countries) if within_countries is not None and len(within_countries) != 0 else None

    def __headers(self, accept_type: AcceptType) -> Dict[str, str]:
        return {
            'X-Application-Id': self.__app_id,
            'X-Api-Key': self.__api_key,
            'User-Agent': 'Travel Time Python SDK',
            'Content-Type': 'application/json',
            'Accept': accept_type.value
        }
