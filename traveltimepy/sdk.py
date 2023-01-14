from datetime import datetime
from typing import List, Optional, Dict, Union

from traveltime.transportation import PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain

from traveltimepy.dto.responses.time_filter_proto import TimeFilterProtoResponse
from traveltimepy.dto.requests.time_filter_proto import Country, ProtoTransportation

from traveltimepy import AcceptType
from traveltimepy.dto import Location, Coordinates, LocationId
from traveltimepy.dto.requests import Rectangle, Property, FullRange, Range

from traveltimepy.dto.requests.supported_locations import SupportedLocationsRequest
from traveltimepy.dto.requests.time_filter_fast import Transportation

from traveltimepy.dto.requests.zones import ZonesProperty
from traveltimepy.dto.responses.map_info import MapInfoResponse
from traveltimepy.dto.responses.postcodes import PostcodesResponse
from traveltimepy.dto.responses.routes import RoutesResponse
from traveltimepy.dto.responses.supported_locations import SupportedLocationsResponse
from traveltimepy.dto.responses.time_filter import TimeFilterResponse
from traveltimepy.dto.responses.time_filter_fast import TimeFilterFastResponse
from traveltimepy.dto.responses.time_map import TimeMapResponse
from traveltimepy.dto.responses.zones import DistrictsResponse, SectorsResponse
from traveltimepy.itertools import join_opt
from traveltimepy.mapper import (
    create_time_filter,
    create_time_filter_fast,
    create_postcodes,
    create_districts,
    create_sectors,
    create_routes, create_proto_request, create_time_map
)
from traveltimepy.http import (
    send_get,
    send_get_async,
    send_post,
    send_post_async
)

from geojson_pydantic import FeatureCollection

from traveltimepy.proto_http import send_proto, send_proto_async


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
        return send_post(
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
        travel_time: int = 1800,
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

    async def districts_async(
        self,
        coordinates: List[Coordinates],
        transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain],
        travel_time: int = 1800,
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        reachable_postcodes_threshold=0.1,
        properties: Optional[List[ZonesProperty]] = None,
        full_range: Optional[FullRange] = None
    ) -> DistrictsResponse:
        return await send_post_async(
            DistrictsResponse,
            'time-filter/postcode-districts',
            self.__headers(AcceptType.JSON),
            create_districts(
                coordinates,
                transportation,
                travel_time,
                departure_time,
                arrival_time,
                reachable_postcodes_threshold,
                properties,
                full_range
            )
        )

    def districts(
        self,
        coordinates: List[Coordinates],
        transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain],
        travel_time: int = 1800,
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        reachable_postcodes_threshold=0.1,
        properties: Optional[List[ZonesProperty]] = None,
        full_range: Optional[FullRange] = None
    ) -> DistrictsResponse:
        return send_post(
            DistrictsResponse,
            'time-filter/postcode-districts',
            self.__headers(AcceptType.JSON),
            create_districts(
                coordinates,
                transportation,
                travel_time,
                departure_time,
                arrival_time,
                reachable_postcodes_threshold,
                properties,
                full_range
            )
        )

    async def sectors_async(
        self,
        coordinates: List[Coordinates],
        transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain],
        travel_time: int = 1800,
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        reachable_postcodes_threshold=0.1,
        properties: Optional[List[ZonesProperty]] = None,
        full_range: Optional[FullRange] = None
    ) -> SectorsResponse:
        return await send_post_async(
            SectorsResponse,
            'time-filter/postcode-sectors',
            self.__headers(AcceptType.JSON),
            create_sectors(
                coordinates,
                transportation,
                travel_time,
                departure_time,
                arrival_time,
                reachable_postcodes_threshold,
                properties,
                full_range
            )
        )

    def sectors(
        self,
        coordinates: List[Coordinates],
        transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain],
        travel_time: int = 1800,
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        reachable_postcodes_threshold=0.1,
        properties: Optional[List[ZonesProperty]] = None,
        full_range: Optional[FullRange] = None
    ) -> SectorsResponse:
        return send_post(
            SectorsResponse,
            'time-filter/postcode-sectors',
            self.__headers(AcceptType.JSON),
            create_sectors(
                coordinates,
                transportation,
                travel_time,
                departure_time,
                arrival_time,
                reachable_postcodes_threshold,
                properties,
                full_range
            )
        )

    def routes(
        self,
        locations: List[Location],
        searches: Dict[LocationId, List[LocationId]],
        transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain],
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        properties: Optional[List[Property]] = None,
        full_range: Optional[FullRange] = None
    ) -> RoutesResponse:
        return send_post(
            RoutesResponse,
            'routes',
            self.__headers(AcceptType.JSON),
            create_routes(
                locations,
                searches,
                transportation,
                departure_time,
                arrival_time,
                properties,
                full_range
            )
        )

    async def routes_async(
        self,
        locations: List[Location],
        searches: Dict[LocationId, List[LocationId]],
        transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain],
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        properties: Optional[List[Property]] = None,
        full_range: Optional[FullRange] = None
    ) -> RoutesResponse:
        return send_post(
            RoutesResponse,
            'routes',
            self.__headers(AcceptType.JSON),
            create_routes(
                locations,
                searches,
                transportation,
                departure_time,
                arrival_time,
                properties,
                full_range
            )
        )

    def time_filter_proto(
        self,
        origin: Coordinates,
        destinations: List[Coordinates],
        country: Country,
        transportation: ProtoTransportation,
        travel_time: int,
    ) -> TimeFilterProtoResponse:
        return send_proto(
            f'https://proto.api.traveltimeapp.com/api/v2/{country.value}/time-filter/fast/{transportation.name}',
            self.__proto_headers(),
            create_proto_request(origin, destinations, transportation, travel_time),
            self.__app_id,
            self.__api_key
        )

    async def time_filter_proto_async(
        self,
        origin: Coordinates,
        destinations: List[Coordinates],
        country: Country,
        transportation: ProtoTransportation,
        travel_time: int,
    ) -> TimeFilterProtoResponse:
        return await send_proto_async(
            f'https://proto.api.traveltimeapp.com/api/v2/{country.value}/time-filter/fast/{transportation.name}',
            self.__proto_headers(),
            create_proto_request(origin, destinations, transportation, travel_time),
            self.__app_id,
            self.__api_key
        )

    def time_map(
        self,
        coordinates: List[Coordinates],
        transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain],
        arrival_time: Optional[datetime] = None,
        departure_time: Optional[datetime] = None,
        travel_time: int = 3600,
        search_range: Optional[Range] = None
    ) -> TimeMapResponse:
        return send_post(
            TimeMapResponse,
            'time-map',
            self.__headers(AcceptType.JSON),
            create_time_map(
                coordinates,
                transportation,
                travel_time,
                arrival_time,
                departure_time,
                search_range
            )
        )

    async def time_map_async(
        self,
        coordinates: List[Coordinates],
        transportation: Union[PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain],
        arrival_time: Optional[datetime] = None,
        departure_time: Optional[datetime] = None,
        travel_time: int = 3600,
        search_range: Optional[Range] = None
    ) -> TimeMapResponse:
        return await send_post_async(
            TimeMapResponse,
            'time-map',
            self.__headers(AcceptType.JSON),
            create_time_map(
                coordinates,
                transportation,
                travel_time,
                arrival_time,
                departure_time,
                search_range
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

    @staticmethod
    def __proto_headers() -> Dict[str, str]:
        return {
            'Content-Type': AcceptType.OCTET_STREAM.value,
            'User-Agent': 'Travel Time Python SDK'
        }

    def __headers(self, accept_type: AcceptType) -> Dict[str, str]:
        return {
            'X-Application-Id': self.__app_id,
            'X-Api-Key': self.__api_key,
            'User-Agent': 'Travel Time Python SDK',
            'Content-Type': 'application/json',
            'Accept': accept_type.value
        }
