from datetime import datetime
from typing import List, Optional, Dict, Union

from traveltimepy.dto.common import (
    Location,
    Coordinates,
    Rectangle,
    Property,
    FullRange,
    Range,
    LevelOfDetail,
    PropertyProto,
    DepartureTime,
    ArrivalTime,
)
from traveltimepy.dto.responses.time_map_wkt import (
    TimeMapWKTResponse,
)
from traveltimepy.dto.responses.time_filter_proto import TimeFilterProtoResponse
from traveltimepy.dto.transportation import (
    PublicTransport,
    Driving,
    Ferry,
    Walking,
    Cycling,
    DrivingTrain,
    CyclingPublicTransport,
)
from traveltimepy.dto.requests.postcodes_zones import ZonesProperty
from traveltimepy.dto.requests.time_filter_proto import (
    ProtoCountry,
    ProtoTransportation,
)
from traveltimepy.dto.requests.time_filter_fast import Transportation
from traveltimepy.errors import ApiError

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
    create_time_map_geojson,
    create_time_map_wkt,
)

from traveltimepy.proto_http import send_proto_async
from traveltimepy.http import (
    send_get_async,
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
        proto_host: str = "proto.api.traveltimeapp.com",
        timeout: int = 300,
    ) -> None:
        self._app_id = app_id
        self._api_key = api_key
        self._sdk_params = SdkParams(
            host,
            proto_host,
            limit_per_host,
            rate_limit,
            time_window,
            retry_attempts,
            timeout,
        )

    async def time_filter_async(
        self,
        locations: List[Location],
        search_ids: Dict[str, List[str]],
        transportation: Union[
            PublicTransport,
            Driving,
            Ferry,
            Walking,
            Cycling,
            DrivingTrain,
            CyclingPublicTransport,
        ],
        properties: Optional[List[Property]] = None,
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        travel_time: int = 3600,
        range: Optional[FullRange] = None,
    ) -> List[TimeFilterResult]:
        time_info = get_time_info(departure_time, arrival_time)

        resp = await send_post_async(
            TimeFilterResponse,
            "time-filter",
            self._headers(AcceptType.JSON),
            create_time_filter(
                locations,
                search_ids,
                transportation,
                properties,
                time_info,
                travel_time,
                range,
            ),
            self._sdk_params,
        )

        return resp.results

    async def map_info_async(self) -> List[Map]:
        res = await send_get_async(
            MapInfoResponse,
            "map-info",
            self._headers(AcceptType.JSON),
            self._sdk_params,
        )
        return res.maps

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
            self._headers(AcceptType.JSON),
            self._sdk_params,
            self._geocoding_params(
                query,
                limit,
                within_countries,
                format_name,
                format_exclude_country,
                bounds,
            ),
        )

    async def geocoding_reverse_async(
        self,
        lat: float,
        lng: float,
    ) -> FeatureCollection:
        return await send_get_async(
            FeatureCollection,
            "geocoding/reverse",
            self._headers(AcceptType.JSON),
            self._sdk_params,
            self._geocoding_reverse_params(lat, lng),
        )

    async def supported_locations_async(
        self,
        locations: List[Location],
    ) -> SupportedLocationsResponse:
        return await send_post_async(
            SupportedLocationsResponse,
            "supported-locations",
            self._headers(AcceptType.JSON),
            SupportedLocationsRequest(locations=locations),
            self._sdk_params,
        )

    async def time_filter_fast_async(
        self,
        locations: List[Location],
        search_ids: Dict[str, List[str]],
        transportation: Transportation,
        travel_time: int = 3600,
        properties: Optional[List[Property]] = None,
        one_to_many: bool = True,
    ) -> List[TimeFilterFastResult]:
        resp = await send_post_async(
            TimeFilterFastResponse,
            "time-filter/fast",
            self._headers(AcceptType.JSON),
            create_time_filter_fast(
                locations,
                search_ids,
                transportation,
                travel_time,
                properties,
                one_to_many,
            ),
            self._sdk_params,
        )
        return resp.results

    async def postcodes_async(
        self,
        coordinates: List[Coordinates],
        transportation: Union[
            PublicTransport,
            Driving,
            Ferry,
            Walking,
            Cycling,
            DrivingTrain,
            CyclingPublicTransport,
        ],
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        travel_time: int = 1800,
        properties: Optional[List[Property]] = None,
        range: Optional[FullRange] = None,
    ) -> List[PostcodesResult]:
        time_info = get_time_info(departure_time, arrival_time)

        resp = await send_post_async(
            PostcodesResponse,
            "time-filter/postcodes",
            self._headers(AcceptType.JSON),
            create_postcodes(
                coordinates,
                time_info,
                transportation,
                travel_time,
                properties,
                range,
            ),
            self._sdk_params,
        )
        return resp.results

    async def postcodes_districts_async(
        self,
        coordinates: List[Coordinates],
        transportation: Union[
            PublicTransport,
            Driving,
            Ferry,
            Walking,
            Cycling,
            DrivingTrain,
            CyclingPublicTransport,
        ],
        travel_time: int = 1800,
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        reachable_postcodes_threshold=0.1,
        properties: Optional[List[ZonesProperty]] = None,
        range: Optional[FullRange] = None,
    ) -> List[PostcodesDistrictsResult]:
        time_info = get_time_info(departure_time, arrival_time)

        res = await send_post_async(
            PostcodesDistrictsResponse,
            "time-filter/postcode-districts",
            self._headers(AcceptType.JSON),
            create_districts(
                coordinates,
                transportation,
                travel_time,
                time_info,
                reachable_postcodes_threshold,
                properties,
                range,
            ),
            self._sdk_params,
        )
        return res.results

    async def postcodes_sectors_async(
        self,
        coordinates: List[Coordinates],
        transportation: Union[
            PublicTransport,
            Driving,
            Ferry,
            Walking,
            Cycling,
            DrivingTrain,
            CyclingPublicTransport,
        ],
        travel_time: int = 1800,
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        reachable_postcodes_threshold=0.1,
        properties: Optional[List[ZonesProperty]] = None,
        range: Optional[FullRange] = None,
    ) -> List[PostcodesSectorsResult]:
        time_info = get_time_info(departure_time, arrival_time)

        resp = await send_post_async(
            PostcodesSectorsResponse,
            "time-filter/postcode-sectors",
            self._headers(AcceptType.JSON),
            create_sectors(
                coordinates,
                transportation,
                travel_time,
                time_info,
                reachable_postcodes_threshold,
                properties,
                range,
            ),
            self._sdk_params,
        )
        return resp.results

    async def routes_async(
        self,
        locations: List[Location],
        search_ids: Dict[str, List[str]],
        transportation: Union[
            PublicTransport,
            Driving,
            Ferry,
            Walking,
            Cycling,
            DrivingTrain,
            CyclingPublicTransport,
        ],
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        properties: Optional[List[Property]] = None,
        range: Optional[FullRange] = None,
    ) -> List[RoutesResult]:
        time_info = get_time_info(departure_time, arrival_time)

        resp = await send_post_async(
            RoutesResponse,
            "routes",
            self._headers(AcceptType.JSON),
            create_routes(
                locations,
                search_ids,
                transportation,
                time_info,
                properties,
                range,
            ),
            self._sdk_params,
        )
        return resp.results

    async def time_filter_proto_async(
        self,
        origin: Coordinates,
        destinations: List[Coordinates],
        country: ProtoCountry,
        transportation: ProtoTransportation,
        travel_time: int,
        one_to_many: bool = True,
        properties: Optional[List[PropertyProto]] = None,
    ) -> TimeFilterProtoResponse:
        resp = await send_proto_async(
            f"https://{self._sdk_params.proto_host}/api/v2/{country.value}/time-filter/fast/{transportation.value.name}",
            # noqa
            self._proto_headers(),
            create_proto_request(
                origin,
                destinations,
                transportation,
                properties,
                travel_time,
                one_to_many,
            ),
            self._app_id,
            self._api_key,
            self._sdk_params.timeout,
        )
        return resp

    async def intersection_async(
        self,
        coordinates: List[Coordinates],
        transportation: Union[
            PublicTransport,
            Driving,
            Ferry,
            Walking,
            Cycling,
            DrivingTrain,
            CyclingPublicTransport,
        ],
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        travel_time: int = 3600,
        search_range: Optional[Range] = None,
        level_of_detail: Optional[LevelOfDetail] = None,
    ) -> TimeMapResult:
        time_info = get_time_info(departure_time, arrival_time)

        resp = await send_post_async(
            TimeMapResponse,
            "time-map",
            self._headers(AcceptType.JSON),
            create_intersection(
                coordinates,
                transportation,
                travel_time,
                time_info,
                search_range,
                level_of_detail,
            ),
            self._sdk_params,
        )
        return resp.results[0]

    async def union_async(
        self,
        coordinates: List[Coordinates],
        transportation: Union[
            PublicTransport,
            Driving,
            Ferry,
            Walking,
            Cycling,
            DrivingTrain,
            CyclingPublicTransport,
        ],
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        travel_time: int = 3600,
        search_range: Optional[Range] = None,
        level_of_detail: Optional[LevelOfDetail] = None,
    ) -> TimeMapResult:
        time_info = get_time_info(departure_time, arrival_time)

        resp = await send_post_async(
            TimeMapResponse,
            "time-map",
            self._headers(AcceptType.JSON),
            create_union(
                coordinates,
                transportation,
                travel_time,
                time_info,
                search_range,
                level_of_detail,
            ),
            self._sdk_params,
        )

        return resp.results[0]

    async def time_map_async(
        self,
        coordinates: List[Coordinates],
        transportation: Union[
            PublicTransport,
            Driving,
            Ferry,
            Walking,
            Cycling,
            DrivingTrain,
            CyclingPublicTransport,
        ],
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        travel_time: int = 3600,
        search_range: Optional[Range] = None,
        level_of_detail: Optional[LevelOfDetail] = None,
    ) -> List[TimeMapResult]:
        time_info = get_time_info(departure_time, arrival_time)

        resp = await send_post_async(
            TimeMapResponse,
            "time-map",
            self._headers(AcceptType.JSON),
            create_time_map(
                coordinates,
                transportation,
                travel_time,
                time_info,
                search_range,
                level_of_detail,
            ),
            self._sdk_params,
        )
        return resp.results

    async def time_map_geojson_async(
        self,
        coordinates: List[Coordinates],
        transportation: Union[
            PublicTransport,
            Driving,
            Ferry,
            Walking,
            Cycling,
            DrivingTrain,
            CyclingPublicTransport,
        ],
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        travel_time: int = 3600,
        search_range: Optional[Range] = None,
        level_of_detail: Optional[LevelOfDetail] = None,
    ) -> FeatureCollection:
        time_info = get_time_info(departure_time, arrival_time)

        resp = await send_post_async(
            FeatureCollection,
            "time-map",
            self._headers(AcceptType.GEO_JSON),
            create_time_map_geojson(
                coordinates,
                transportation,
                travel_time,
                time_info,
                search_range,
                level_of_detail,
            ),
            self._sdk_params,
        )
        return resp

    async def time_map_wkt_async(
        self,
        coordinates: List[Coordinates],
        transportation: Union[
            PublicTransport,
            Driving,
            Ferry,
            Walking,
            Cycling,
            DrivingTrain,
            CyclingPublicTransport,
        ],
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        travel_time: int = 3600,
        search_range: Optional[Range] = None,
        level_of_detail: Optional[LevelOfDetail] = None,
    ) -> TimeMapWKTResponse:
        time_info = get_time_info(departure_time, arrival_time)

        resp = await send_post_async(
            TimeMapWKTResponse,
            "time-map",
            self._headers(AcceptType.WKT),
            create_time_map_wkt(
                coordinates,
                transportation,
                travel_time,
                time_info,
                search_range,
                level_of_detail,
            ),
            self._sdk_params,
        )
        return resp

    async def time_map_wkt_no_holes_async(
        self,
        coordinates: List[Coordinates],
        transportation: Union[
            PublicTransport,
            Driving,
            Ferry,
            Walking,
            Cycling,
            DrivingTrain,
            CyclingPublicTransport,
        ],
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        travel_time: int = 3600,
        search_range: Optional[Range] = None,
        level_of_detail: Optional[LevelOfDetail] = None,
    ) -> TimeMapWKTResponse:
        time_info = get_time_info(departure_time, arrival_time)

        resp = await send_post_async(
            TimeMapWKTResponse,
            "time-map",
            self._headers(AcceptType.WKT_NO_HOLES),
            create_time_map_wkt(
                coordinates,
                transportation,
                travel_time,
                time_info,
                search_range,
                level_of_detail,
            ),
            self._sdk_params,
        )
        return resp

    @staticmethod
    def _geocoding_reverse_params(lat: float, lng: float) -> Dict[str, str]:
        full_query = {"lat": lat, "lng": lng}
        return {
            key: str(value) for (key, value) in full_query.items() if value is not None
        }

    @staticmethod
    def _geocoding_params(
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
    def _proto_headers() -> Dict[str, str]:
        return {
            "Content-Type": AcceptType.OCTET_STREAM.value,
            "User-Agent": f"Travel Time Python SDK {__version__}",
        }

    def _headers(self, accept_type: AcceptType) -> Dict[str, str]:
        return {
            "X-Application-Id": self._app_id,
            "X-Api-Key": self._api_key,
            "User-Agent": f"Travel Time Python SDK {__version__}",
            "Content-Type": "application/json",
            "Accept": accept_type.value,
        }


def get_time_info(departure_time: Optional[datetime], arrival_time: Optional[datetime]):
    if departure_time and arrival_time:
        raise ApiError("arrival_time and departure_time cannot be both specified")

    time_info = None
    if departure_time:
        time_info = DepartureTime(departure_time)
    elif arrival_time:
        time_info = ArrivalTime(arrival_time)

    return time_info
