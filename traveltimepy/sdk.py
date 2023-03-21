from datetime import datetime
from typing import List, Optional, Dict, Union

from traveltimepy.dto.common import (
    Location,
    Coordinates,
    Rectangle,
    Property,
    FullRange,
    Range,
)
from traveltimepy.dto.transportation import (
    PublicTransport,
    Driving,
    Ferry,
    Walking,
    Cycling,
    DrivingTrain,
)
from traveltimepy.dto.requests.postcodes_zones import ZonesProperty
from traveltimepy.dto.requests.time_filter_proto import (
    ProtoCountry,
    ProtoTransportation,
)
from traveltimepy.dto.requests.time_filter_fast import Transportation

from traveltimepy.version import __version__
from traveltimepy.accept_type import AcceptType
from traveltimepy.itertools import join_opt
from traveltimepy.dto.requests.supported_locations import SupportedLocationsRequest

from traveltimepy.dto.responses.map_info import MapInfoResponse, Map
from traveltimepy.dto.responses.postcodes import PostcodesResponse, PostcodesResult
from traveltimepy.dto.responses.routes import RoutesResponse, RoutesResult
from traveltimepy.dto.responses.supported_locations import SupportedLocationsResponse
from traveltimepy.dto.responses.time_filter import TimeFilterResponse, TimeFilterResult
from traveltimepy.dto.responses.time_filter_fast import (
    TimeFilterFastResponse,
    TimeFilterFastResult,
)
from traveltimepy.dto.responses.time_map import TimeMapResponse, TimeMapResult
from traveltimepy.dto.responses.zones import (
    PostcodesDistrictsResponse,
    PostcodesSectorsResponse,
    PostcodesDistrictsResult,
    PostcodesSectorsResult,
)

from traveltimepy.mapper import (
    create_time_filter,
    create_time_filter_fast,
    create_postcodes,
    create_districts,
    create_sectors,
    create_routes,
    create_proto_request,
    create_time_map,
    create_intersection,
    create_union,
)

from traveltimepy.proto_http import send_proto, send_proto_async
from traveltimepy.http import (
    send_get,
    send_get_async,
    send_post,
    send_post_async,
    SdkParams,
)

from geojson_pydantic import FeatureCollection


class TravelTimeSdk:
    def __init__(
        self,
        app_id: str,
        api_key: str,
        limit_per_host: int = 2,
        rate_limit: int = 60,
        time_window: int = 60,
        retry_attempts: int = 2,
        host: str = "api.traveltimeapp.com",
    ) -> None:
        self.__app_id = app_id
        self.__api_key = api_key
        self.__sdk_params = SdkParams(
            host, limit_per_host, rate_limit, time_window, retry_attempts
        )

    async def time_filter_async(
        self,
        locations: List[Location],
        search_ids: Dict[str, List[str]],
        transportation: Union[
            PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain
        ],
        properties: Optional[List[Property]] = None,
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        travel_time: int = 3600,
        range: Optional[FullRange] = None,
    ) -> List[TimeFilterResult]:
        resp = await send_post_async(
            TimeFilterResponse,
            "time-filter",
            self.__headers(AcceptType.JSON),
            create_time_filter(
                locations,
                search_ids,
                transportation,
                properties,
                departure_time,
                arrival_time,
                travel_time,
                range,
            ),
            self.__sdk_params,
        )

        return resp.results

    def time_filter(
        self,
        locations: List[Location],
        search_ids: Dict[str, List[str]],
        transportation: Union[
            PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain
        ],
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        properties: Optional[List[Property]] = None,
        travel_time: int = 3600,
        range: Optional[FullRange] = None,
    ) -> List[TimeFilterResult]:
        return send_post(
            TimeFilterResponse,
            "time-filter",
            self.__headers(AcceptType.JSON),
            create_time_filter(
                locations,
                search_ids,
                transportation,
                properties,
                departure_time,
                arrival_time,
                travel_time,
                range,
            ),
            self.__sdk_params,
        ).results

    async def map_info_async(self) -> List[Map]:
        res = await send_get_async(
            MapInfoResponse,
            "map-info",
            self.__headers(AcceptType.JSON),
            self.__sdk_params,
        )
        return res.maps

    def map_info(self) -> List[Map]:
        return send_get(
            MapInfoResponse,
            "map-info",
            self.__headers(AcceptType.JSON),
            self.__sdk_params,
        ).maps

    async def geocoding_async(
        self,
        query: str,
        limit: Optional[int] = None,
        within_countries: Optional[List[str]] = None,
        format_name: Optional[bool] = None,
        format_exclude_country: Optional[bool] = None,
        bounds: Optional[Rectangle] = None,
    ) -> FeatureCollection:
        return await send_get_async(
            FeatureCollection,
            "geocoding/search",
            self.__headers(AcceptType.JSON),
            self.__sdk_params,
            self.__geocoding_params(
                query,
                limit,
                within_countries,
                format_name,
                format_exclude_country,
                bounds,
            ),
        )

    def geocoding(
        self,
        query: str,
        limit: Optional[int] = None,
        within_countries: Optional[List[str]] = None,
        format_name: Optional[bool] = None,
        format_exclude_country: Optional[bool] = None,
        bounds: Optional[Rectangle] = None,
    ) -> FeatureCollection:
        return send_get(
            FeatureCollection,
            "geocoding/search",
            self.__headers(AcceptType.JSON),
            self.__sdk_params,
            self.__geocoding_params(
                query,
                limit,
                within_countries,
                format_name,
                format_exclude_country,
                bounds,
            ),
        )

    async def geocoding_reverse_async(
        self, lat: float, lng: float
    ) -> FeatureCollection:
        return await send_get_async(
            FeatureCollection,
            "geocoding/reverse",
            self.__headers(AcceptType.JSON),
            self.__sdk_params,
            self.__geocoding_reverse_params(lat, lng),
        )

    def geocoding_reverse(self, lat: float, lng: float) -> FeatureCollection:
        return send_get(
            FeatureCollection,
            "geocoding/reverse",
            self.__headers(AcceptType.JSON),
            self.__sdk_params,
            self.__geocoding_reverse_params(lat, lng),
        )

    async def supported_locations_async(
        self, locations: List[Location]
    ) -> SupportedLocationsResponse:
        return await send_post_async(
            SupportedLocationsResponse,
            "supported-locations",
            self.__headers(AcceptType.JSON),
            SupportedLocationsRequest(locations=locations),
            self.__sdk_params,
        )

    def supported_locations(
        self, locations: List[Location]
    ) -> SupportedLocationsResponse:
        return send_post(
            SupportedLocationsResponse,
            "supported-locations",
            self.__headers(AcceptType.JSON),
            SupportedLocationsRequest(locations=locations),
            self.__sdk_params,
        )

    async def time_filter_fast_async(
        self,
        locations: List[Location],
        search_ids: Dict[str, List[str]],
        transportation: Transportation,
        travel_time: int = 3600,
        properties: Optional[List[Property]] = None,
        one_to_many: bool = False,
    ) -> List[TimeFilterFastResult]:
        resp = await send_post_async(
            TimeFilterFastResponse,
            "time-filter/fast",
            self.__headers(AcceptType.JSON),
            create_time_filter_fast(
                locations,
                search_ids,
                transportation,
                travel_time,
                properties,
                one_to_many,
            ),
            self.__sdk_params,
        )
        return resp.results

    def time_filter_fast(
        self,
        locations: List[Location],
        search_ids: Dict[str, List[str]],
        transportation: Transportation,
        travel_time: int = 3600,
        properties: Optional[List[Property]] = None,
        one_to_many: bool = False,
    ) -> List[TimeFilterFastResult]:
        return send_post(
            TimeFilterFastResponse,
            "time-filter/fast",
            self.__headers(AcceptType.JSON),
            create_time_filter_fast(
                locations,
                search_ids,
                transportation,
                travel_time,
                properties,
                one_to_many,
            ),
            self.__sdk_params,
        ).results

    async def postcodes_async(
        self,
        coordinates: List[Coordinates],
        transportation: Union[
            PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain
        ],
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        travel_time: int = 1800,
        properties: Optional[List[Property]] = None,
        range: Optional[FullRange] = None,
    ) -> List[PostcodesResult]:
        resp = await send_post_async(
            PostcodesResponse,
            "time-filter/postcodes",
            self.__headers(AcceptType.JSON),
            create_postcodes(
                coordinates,
                departure_time,
                arrival_time,
                transportation,
                travel_time,
                properties,
                range,
            ),
            self.__sdk_params,
        )
        return resp.results

    def postcodes(
        self,
        coordinates: List[Coordinates],
        transportation: Union[
            PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain
        ],
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        travel_time: int = 1800,
        properties: Optional[List[Property]] = None,
        range: Optional[FullRange] = None,
    ) -> List[PostcodesResult]:
        return send_post(
            PostcodesResponse,
            "time-filter/postcodes",
            self.__headers(AcceptType.JSON),
            create_postcodes(
                coordinates,
                departure_time,
                arrival_time,
                transportation,
                travel_time,
                properties,
                range,
            ),
            self.__sdk_params,
        ).results

    async def postcodes_districts_async(
        self,
        coordinates: List[Coordinates],
        transportation: Union[
            PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain
        ],
        travel_time: int = 1800,
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        reachable_postcodes_threshold=0.1,
        properties: Optional[List[ZonesProperty]] = None,
        range: Optional[FullRange] = None,
    ) -> List[PostcodesDistrictsResult]:
        res = await send_post_async(
            PostcodesDistrictsResponse,
            "time-filter/postcode-districts",
            self.__headers(AcceptType.JSON),
            create_districts(
                coordinates,
                transportation,
                travel_time,
                departure_time,
                arrival_time,
                reachable_postcodes_threshold,
                properties,
                range,
            ),
            self.__sdk_params,
        )
        return res.results

    def postcode_districts(
        self,
        coordinates: List[Coordinates],
        transportation: Union[
            PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain
        ],
        travel_time: int = 1800,
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        reachable_postcodes_threshold=0.1,
        properties: Optional[List[ZonesProperty]] = None,
        range: Optional[FullRange] = None,
    ) -> List[PostcodesDistrictsResult]:
        return send_post(
            PostcodesDistrictsResponse,
            "time-filter/postcode-districts",
            self.__headers(AcceptType.JSON),
            create_districts(
                coordinates,
                transportation,
                travel_time,
                departure_time,
                arrival_time,
                reachable_postcodes_threshold,
                properties,
                range,
            ),
            self.__sdk_params,
        ).results

    async def postcodes_sectors_async(
        self,
        coordinates: List[Coordinates],
        transportation: Union[
            PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain
        ],
        travel_time: int = 1800,
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        reachable_postcodes_threshold=0.1,
        properties: Optional[List[ZonesProperty]] = None,
        range: Optional[FullRange] = None,
    ) -> List[PostcodesSectorsResult]:
        resp = await send_post_async(
            PostcodesSectorsResponse,
            "time-filter/postcode-sectors",
            self.__headers(AcceptType.JSON),
            create_sectors(
                coordinates,
                transportation,
                travel_time,
                departure_time,
                arrival_time,
                reachable_postcodes_threshold,
                properties,
                range,
            ),
            self.__sdk_params,
        )
        return resp.results

    def postcode_sectors(
        self,
        coordinates: List[Coordinates],
        transportation: Union[
            PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain
        ],
        travel_time: int = 1800,
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        reachable_postcodes_threshold=0.1,
        properties: Optional[List[ZonesProperty]] = None,
        range: Optional[FullRange] = None,
    ) -> List[PostcodesSectorsResult]:
        return send_post(
            PostcodesSectorsResponse,
            "time-filter/postcode-sectors",
            self.__headers(AcceptType.JSON),
            create_sectors(
                coordinates,
                transportation,
                travel_time,
                departure_time,
                arrival_time,
                reachable_postcodes_threshold,
                properties,
                range,
            ),
            self.__sdk_params,
        ).results

    def routes(
        self,
        locations: List[Location],
        search_ids: Dict[str, List[str]],
        transportation: Union[
            PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain
        ],
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        properties: Optional[List[Property]] = None,
        range: Optional[FullRange] = None,
    ) -> List[RoutesResult]:
        return send_post(
            RoutesResponse,
            "routes",
            self.__headers(AcceptType.JSON),
            create_routes(
                locations,
                search_ids,
                transportation,
                departure_time,
                arrival_time,
                properties,
                range,
            ),
            self.__sdk_params,
        ).results

    async def routes_async(
        self,
        locations: List[Location],
        search_ids: Dict[str, List[str]],
        transportation: Union[
            PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain
        ],
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        properties: Optional[List[Property]] = None,
        range: Optional[FullRange] = None,
    ) -> List[RoutesResult]:
        resp = await send_post_async(
            RoutesResponse,
            "routes",
            self.__headers(AcceptType.JSON),
            create_routes(
                locations,
                search_ids,
                transportation,
                departure_time,
                arrival_time,
                properties,
                range,
            ),
            self.__sdk_params,
        )
        return resp.results

    def time_filter_proto(
        self,
        origin: Coordinates,
        destinations: List[Coordinates],
        country: ProtoCountry,
        transportation: ProtoTransportation,
        travel_time: int,
    ) -> List[int]:
        return send_proto(
            f"https://proto.api.traveltimeapp.com/api/v2/{country.value}/time-filter/fast/{transportation.value.name}",  # noqa
            self.__proto_headers(),
            create_proto_request(origin, destinations, transportation, travel_time),
            self.__app_id,
            self.__api_key,
        ).travel_times

    async def time_filter_proto_async(
        self,
        origin: Coordinates,
        destinations: List[Coordinates],
        country: ProtoCountry,
        transportation: ProtoTransportation,
        travel_time: int,
    ) -> List[int]:
        resp = await send_proto_async(
            f"https://proto.api.traveltimeapp.com/api/v2/{country.value}/time-filter/fast/{transportation.name}",  # noqa
            self.__proto_headers(),
            create_proto_request(origin, destinations, transportation, travel_time),
            self.__app_id,
            self.__api_key,
        )
        return resp.travel_times

    def time_map(
        self,
        coordinates: List[Coordinates],
        transportation: Union[
            PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain
        ],
        arrival_time: Optional[datetime] = None,
        departure_time: Optional[datetime] = None,
        travel_time: int = 3600,
        search_range: Optional[Range] = None,
    ) -> List[TimeMapResult]:
        return send_post(
            TimeMapResponse,
            "time-map",
            self.__headers(AcceptType.JSON),
            create_time_map(
                coordinates,
                transportation,
                travel_time,
                arrival_time,
                departure_time,
                search_range,
            ),
            self.__sdk_params,
        ).results

    def intersection(
        self,
        coordinates: List[Coordinates],
        transportation: Union[
            PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain
        ],
        arrival_time: Optional[datetime] = None,
        departure_time: Optional[datetime] = None,
        travel_time: int = 3600,
        search_range: Optional[Range] = None,
    ) -> TimeMapResult:
        return send_post(
            TimeMapResponse,
            "time-map",
            self.__headers(AcceptType.JSON),
            create_intersection(
                coordinates,
                transportation,
                travel_time,
                arrival_time,
                departure_time,
                search_range,
            ),
            self.__sdk_params,
        ).results[0]

    async def intersection_async(
        self,
        coordinates: List[Coordinates],
        transportation: Union[
            PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain
        ],
        arrival_time: Optional[datetime] = None,
        departure_time: Optional[datetime] = None,
        travel_time: int = 3600,
        search_range: Optional[Range] = None,
    ) -> TimeMapResult:
        resp = await send_post_async(
            TimeMapResponse,
            "time-map",
            self.__headers(AcceptType.JSON),
            create_intersection(
                coordinates,
                transportation,
                travel_time,
                arrival_time,
                departure_time,
                search_range,
            ),
            self.__sdk_params,
        )
        return resp.results[0]

    def union(
        self,
        coordinates: List[Coordinates],
        transportation: Union[
            PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain
        ],
        arrival_time: Optional[datetime] = None,
        departure_time: Optional[datetime] = None,
        travel_time: int = 3600,
        search_range: Optional[Range] = None,
    ) -> TimeMapResult:
        return send_post(
            TimeMapResponse,
            "time-map",
            self.__headers(AcceptType.JSON),
            create_union(
                coordinates,
                transportation,
                travel_time,
                arrival_time,
                departure_time,
                search_range,
            ),
            self.__sdk_params,
        ).results[0]

    async def union_async(
        self,
        coordinates: List[Coordinates],
        transportation: Union[
            PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain
        ],
        arrival_time: Optional[datetime] = None,
        departure_time: Optional[datetime] = None,
        travel_time: int = 3600,
        search_range: Optional[Range] = None,
    ) -> TimeMapResult:
        resp = await send_post_async(
            TimeMapResponse,
            "time-map",
            self.__headers(AcceptType.JSON),
            create_union(
                coordinates,
                transportation,
                travel_time,
                arrival_time,
                departure_time,
                search_range,
            ),
            self.__sdk_params,
        )

        return resp.results[0]

    async def time_map_async(
        self,
        coordinates: List[Coordinates],
        transportation: Union[
            PublicTransport, Driving, Ferry, Walking, Cycling, DrivingTrain
        ],
        arrival_time: Optional[datetime] = None,
        departure_time: Optional[datetime] = None,
        travel_time: int = 3600,
        search_range: Optional[Range] = None,
    ) -> List[TimeMapResult]:
        resp = await send_post_async(
            TimeMapResponse,
            "time-map",
            self.__headers(AcceptType.JSON),
            create_time_map(
                coordinates,
                transportation,
                travel_time,
                arrival_time,
                departure_time,
                search_range,
            ),
            self.__sdk_params,
        )
        return resp.results

    @staticmethod
    def __geocoding_reverse_params(lat: float, lng: float) -> Dict[str, str]:
        full_query = {"lat": lat, "lng": lng}
        return {
            key: str(value) for (key, value) in full_query.items() if value is not None
        }

    @staticmethod
    def __geocoding_params(
        query: str,
        limit: Optional[int] = None,
        within_countries: Optional[List[str]] = None,
        format_name: Optional[bool] = None,
        format_exclude_country: Optional[bool] = None,
        bounds: Optional[Rectangle] = None,
    ) -> Dict[str, str]:
        full_query = {
            "query": query,
            "limit": limit,
            "within.country": join_opt(within_countries, ","),
            "format.name": format_name,
            "format.exclude.country": format_exclude_country,
            "bounds": bounds.to_str() if bounds is not None else bounds,
        }
        return {
            key: str(value) for (key, value) in full_query.items() if value is not None
        }

    @staticmethod
    def __proto_headers() -> Dict[str, str]:
        return {
            "Content-Type": AcceptType.OCTET_STREAM.value,
            "User-Agent": f"Travel Time Python SDK {__version__}",
        }

    def __headers(self, accept_type: AcceptType) -> Dict[str, str]:
        return {
            "X-Application-Id": self.__app_id,
            "X-Api-Key": self.__api_key,
            "User-Agent": f"Travel Time Python SDK {__version__}",
            "Content-Type": "application/json",
            "Accept": accept_type.value,
        }
