from datetime import datetime
from typing import List, Optional, Dict, Union

from traveltimepy.dto.common import (
    CellProperty,
    GeohashCentroid,
    H3Centroid,
    Location,
    Coordinates,
    PolygonsFilter,
    Rectangle,
    Property,
    FullRange,
    Range,
    LevelOfDetail,
    PropertyProto,
    DepartureTime,
    ArrivalTime,
    RenderMode,
    Snapping,
)
from traveltimepy.dto.requests import geohash_fast, h3_fast, time_map_fast
from traveltimepy.dto.responses.geohash import GeohashResponse, GeohashResult
from traveltimepy.dto.responses.h3 import H3Response, H3Result
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
    DrivingAndPublicTransportWithDetails,
    ProtoCountry,
    ProtoTransportation,
    PublicTransportWithDetails,
)
from traveltimepy.dto.requests.time_filter_fast import Transportation
from traveltimepy.errors import ApiError

from traveltimepy import __version__
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
    create_distance_map,
    create_geohash,
    create_geohash_fast,
    create_geohash_intersection,
    create_geohash_union,
    create_h3,
    create_h3_fast,
    create_h3_intersection,
    create_h3_union,
    create_time_filter,
    create_time_filter_fast,
    create_postcodes,
    create_districts,
    create_sectors,
    create_routes,
    create_proto_request,
    create_time_map,
    create_time_map_intersection,
    create_time_map_fast,
    create_time_map_fast_geojson,
    create_time_map_fast_wkt,
    create_time_map_union,
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
        user_agent: Optional[str] = None,
    ) -> None:
        self._app_id = app_id
        self._api_key = api_key

        if user_agent is not None:
            self._user_agent = user_agent
        else:
            self._user_agent = f"Travel Time Python SDK {__version__}"

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
        snapping: Optional[Snapping] = None,
        v4_endpoint_path: Optional[str] = None,
    ) -> List[TimeFilterResult]:
        time_info = get_time_info(departure_time, arrival_time)

        resp = await send_post_async(
            TimeFilterResponse,
            v4_endpoint_path or "time-filter",
            self._headers(AcceptType.JSON),
            create_time_filter(
                locations,
                search_ids,
                transportation,
                properties,
                time_info,
                travel_time,
                range,
                snapping,
            ),
            self._sdk_params,
        )

        return resp.results

    async def map_info_async(
        self,
        v4_endpoint_path: Optional[str] = None,
    ) -> List[Map]:
        res = await send_get_async(
            MapInfoResponse,
            v4_endpoint_path or "map-info",
            self._headers(AcceptType.JSON),
            self._sdk_params,
            None,
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
        v4_endpoint_path: Optional[str] = None,
    ) -> FeatureCollection:
        return await send_get_async(
            FeatureCollection,
            v4_endpoint_path or "geocoding/search",
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
        v4_endpoint_path: Optional[str] = None,
    ) -> FeatureCollection:
        return await send_get_async(
            FeatureCollection,
            v4_endpoint_path or "geocoding/reverse",
            self._headers(AcceptType.JSON),
            self._sdk_params,
            self._geocoding_reverse_params(lat, lng),
        )

    async def supported_locations_async(
        self,
        locations: List[Location],
        v4_endpoint_path: Optional[str] = None,
    ) -> SupportedLocationsResponse:
        return await send_post_async(
            SupportedLocationsResponse,
            v4_endpoint_path or "supported-locations",
            self._headers(AcceptType.JSON),
            SupportedLocationsRequest(locations=locations),
            self._sdk_params,
        )

    async def time_map_fast_async(
        self,
        coordinates: List[Coordinates],
        transportation: time_map_fast.Transportation,
        travel_time: int = 3600,
        one_to_many: bool = True,
        level_of_detail: Optional[LevelOfDetail] = None,
        snapping: Optional[Snapping] = None,
        polygons_filter: Optional[PolygonsFilter] = None,
        render_mode: Optional[RenderMode] = None,
        v4_endpoint_path: Optional[str] = None,
    ) -> List[TimeMapResult]:
        resp = await send_post_async(
            TimeMapResponse,
            v4_endpoint_path or "time-map/fast",
            self._headers(AcceptType.JSON),
            create_time_map_fast(
                coordinates,
                transportation,
                travel_time,
                level_of_detail,
                snapping,
                polygons_filter,
                render_mode,
                one_to_many,
            ),
            self._sdk_params,
        )
        return resp.results

    async def time_map_fast_geojson_async(
        self,
        coordinates: List[Coordinates],
        transportation: time_map_fast.Transportation,
        travel_time: int = 3600,
        one_to_many: bool = True,
        level_of_detail: Optional[LevelOfDetail] = None,
        snapping: Optional[Snapping] = None,
        polygons_filter: Optional[PolygonsFilter] = None,
        render_mode: Optional[RenderMode] = None,
        v4_endpoint_path: Optional[str] = None,
    ) -> FeatureCollection:
        resp = await send_post_async(
            FeatureCollection,
            v4_endpoint_path or "time-map/fast",
            self._headers(AcceptType.GEO_JSON),
            create_time_map_fast_geojson(
                coordinates,
                transportation,
                travel_time,
                level_of_detail,
                snapping,
                polygons_filter,
                render_mode,
                one_to_many,
            ),
            self._sdk_params,
        )
        return resp

    async def time_map_fast_wkt_async(
        self,
        coordinates: List[Coordinates],
        transportation: time_map_fast.Transportation,
        travel_time: int = 3600,
        one_to_many: bool = True,
        level_of_detail: Optional[LevelOfDetail] = None,
        snapping: Optional[Snapping] = None,
        polygons_filter: Optional[PolygonsFilter] = None,
        render_mode: Optional[RenderMode] = None,
        v4_endpoint_path: Optional[str] = None,
    ) -> TimeMapWKTResponse:
        resp = await send_post_async(
            TimeMapWKTResponse,
            v4_endpoint_path or "time-map/fast",
            self._headers(AcceptType.WKT),
            create_time_map_fast_wkt(
                coordinates,
                transportation,
                travel_time,
                level_of_detail,
                snapping,
                polygons_filter,
                render_mode,
                one_to_many,
            ),
            self._sdk_params,
        )
        return resp

    async def time_map_fast_wkt_no_holes_async(
        self,
        coordinates: List[Coordinates],
        transportation: time_map_fast.Transportation,
        travel_time: int = 3600,
        one_to_many: bool = True,
        level_of_detail: Optional[LevelOfDetail] = None,
        snapping: Optional[Snapping] = None,
        polygons_filter: Optional[PolygonsFilter] = None,
        render_mode: Optional[RenderMode] = None,
        v4_endpoint_path: Optional[str] = None,
    ) -> TimeMapWKTResponse:
        resp = await send_post_async(
            TimeMapWKTResponse,
            v4_endpoint_path or "time-map/fast",
            self._headers(AcceptType.WKT_NO_HOLES),
            create_time_map_fast_wkt(
                coordinates,
                transportation,
                travel_time,
                level_of_detail,
                snapping,
                polygons_filter,
                render_mode,
                one_to_many,
            ),
            self._sdk_params,
        )
        return resp

    async def h3_fast_async(
        self,
        coordinates: List[Union[Coordinates, H3Centroid]],
        transportation: h3_fast.Transportation,
        properties: List[CellProperty],
        resolution: int,
        travel_time: int = 3600,
        one_to_many: bool = True,
        snapping: Optional[Snapping] = None,
        v4_endpoint_path: Optional[str] = None,
    ) -> List[H3Result]:
        resp = await send_post_async(
            H3Response,
            v4_endpoint_path or "h3/fast",
            self._headers(AcceptType.JSON),
            create_h3_fast(
                coordinates=coordinates,
                transportation=transportation,
                properties=properties,
                resolution=resolution,
                travel_time=travel_time,
                snapping=snapping,
                one_to_many=one_to_many,
            ),
            self._sdk_params,
        )
        return resp.results

    async def geohash_fast_async(
        self,
        coordinates: List[Union[Coordinates, GeohashCentroid]],
        transportation: geohash_fast.Transportation,
        properties: List[CellProperty],
        resolution: int,
        travel_time: int = 3600,
        one_to_many: bool = True,
        snapping: Optional[Snapping] = None,
        v4_endpoint_path: Optional[str] = None,
    ) -> List[GeohashResult]:
        resp = await send_post_async(
            GeohashResponse,
            v4_endpoint_path or "geohash/fast",
            self._headers(AcceptType.JSON),
            create_geohash_fast(
                coordinates=coordinates,
                transportation=transportation,
                properties=properties,
                resolution=resolution,
                travel_time=travel_time,
                snapping=snapping,
                one_to_many=one_to_many,
            ),
            self._sdk_params,
        )
        return resp.results

    async def time_filter_fast_async(
        self,
        locations: List[Location],
        search_ids: Dict[str, List[str]],
        transportation: Transportation,
        travel_time: int = 3600,
        properties: Optional[List[Property]] = None,
        one_to_many: bool = True,
        snapping: Optional[Snapping] = None,
        v4_endpoint_path: Optional[str] = None,
    ) -> List[TimeFilterFastResult]:
        resp = await send_post_async(
            TimeFilterFastResponse,
            v4_endpoint_path or "time-filter/fast",
            self._headers(AcceptType.JSON),
            create_time_filter_fast(
                locations,
                search_ids,
                transportation,
                travel_time,
                properties,
                one_to_many,
                snapping,
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
        v4_endpoint_path: Optional[str] = None,
    ) -> List[PostcodesResult]:
        time_info = get_time_info(departure_time, arrival_time)

        resp = await send_post_async(
            PostcodesResponse,
            v4_endpoint_path or "time-filter/postcodes",
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
        v4_endpoint_path: Optional[str] = None,
    ) -> List[PostcodesDistrictsResult]:
        time_info = get_time_info(departure_time, arrival_time)

        res = await send_post_async(
            PostcodesDistrictsResponse,
            v4_endpoint_path or "time-filter/postcode-districts",
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
        v4_endpoint_path: Optional[str] = None,
    ) -> List[PostcodesSectorsResult]:
        time_info = get_time_info(departure_time, arrival_time)

        resp = await send_post_async(
            PostcodesSectorsResponse,
            v4_endpoint_path or "time-filter/postcode-sectors",
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
        snapping: Optional[Snapping] = None,
        v4_endpoint_path: Optional[str] = None,
    ) -> List[RoutesResult]:
        time_info = get_time_info(departure_time, arrival_time)

        resp = await send_post_async(
            RoutesResponse,
            v4_endpoint_path or "routes",
            self._headers(AcceptType.JSON),
            create_routes(
                locations,
                search_ids,
                transportation,
                time_info,
                properties,
                range,
                snapping,
            ),
            self._sdk_params,
        )
        return resp.results

    async def time_filter_proto_async(
        self,
        origin: Coordinates,
        destinations: List[Coordinates],
        country: ProtoCountry,
        transportation: Union[
            ProtoTransportation,
            PublicTransportWithDetails,
            DrivingAndPublicTransportWithDetails,
        ],
        travel_time: int,
        one_to_many: bool = True,
        properties: Optional[List[PropertyProto]] = None,
    ) -> TimeFilterProtoResponse:
        if isinstance(transportation, ProtoTransportation):
            transportationMode = transportation.value.name
        else:
            transportationMode = transportation.TYPE.value.name

        resp = await send_proto_async(
            f"https://{self._sdk_params.proto_host}/api/v2/{country.value}/time-filter/fast/{transportationMode}",
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

    async def time_map_intersection_async(
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
        snapping: Optional[Snapping] = None,
        polygons_filter: Optional[PolygonsFilter] = None,
        remove_water_bodies: Optional[bool] = None,
        render_mode: Optional[RenderMode] = None,
        v4_endpoint_path: Optional[str] = None,
    ) -> TimeMapResult:
        time_info = get_time_info(departure_time, arrival_time)

        resp = await send_post_async(
            TimeMapResponse,
            v4_endpoint_path or "time-map",
            self._headers(AcceptType.JSON),
            create_time_map_intersection(
                coordinates,
                transportation,
                travel_time,
                time_info,
                search_range,
                level_of_detail,
                snapping,
                polygons_filter,
                remove_water_bodies,
                render_mode,
            ),
            self._sdk_params,
        )
        return resp.results[0]

    # intersection_async was renamed to time_map_intersection_async. Keeping this for legacy users
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
        snapping: Optional[Snapping] = None,
        polygons_filter: Optional[PolygonsFilter] = None,
        remove_water_bodies: Optional[bool] = None,
        render_mode: Optional[RenderMode] = None,
    ) -> TimeMapResult:
        resp = await self.time_map_intersection_async(
            coordinates=coordinates,
            transportation=transportation,
            departure_time=departure_time,
            arrival_time=arrival_time,
            travel_time=travel_time,
            search_range=search_range,
            level_of_detail=level_of_detail,
            snapping=snapping,
            polygons_filter=polygons_filter,
            remove_water_bodies=remove_water_bodies,
            render_mode=render_mode,
        )
        return resp

    async def time_map_union_async(
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
        snapping: Optional[Snapping] = None,
        polygons_filter: Optional[PolygonsFilter] = None,
        remove_water_bodies: Optional[bool] = None,
        render_mode: Optional[RenderMode] = None,
        v4_endpoint_path: Optional[str] = None,
    ) -> TimeMapResult:
        time_info = get_time_info(departure_time, arrival_time)

        resp = await send_post_async(
            TimeMapResponse,
            v4_endpoint_path or "time-map",
            self._headers(AcceptType.JSON),
            create_time_map_union(
                coordinates,
                transportation,
                travel_time,
                time_info,
                search_range,
                level_of_detail,
                snapping,
                polygons_filter,
                remove_water_bodies,
                render_mode,
            ),
            self._sdk_params,
        )

        return resp.results[0]

    # union_async was renamed to time_map_union_async. Keeping this for legacy users
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
        snapping: Optional[Snapping] = None,
        polygons_filter: Optional[PolygonsFilter] = None,
        remove_water_bodies: Optional[bool] = None,
        render_mode: Optional[RenderMode] = None,
    ) -> TimeMapResult:
        resp = await self.time_map_union_async(
            coordinates=coordinates,
            transportation=transportation,
            departure_time=departure_time,
            arrival_time=arrival_time,
            travel_time=travel_time,
            search_range=search_range,
            level_of_detail=level_of_detail,
            snapping=snapping,
            polygons_filter=polygons_filter,
            remove_water_bodies=remove_water_bodies,
            render_mode=render_mode,
        )
        return resp

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
        snapping: Optional[Snapping] = None,
        polygons_filter: Optional[PolygonsFilter] = None,
        remove_water_bodies: Optional[bool] = None,
        render_mode: Optional[RenderMode] = None,
        v4_endpoint_path: Optional[str] = None,
    ) -> List[TimeMapResult]:
        time_info = get_time_info(departure_time, arrival_time)

        resp = await send_post_async(
            TimeMapResponse,
            v4_endpoint_path or "time-map",
            self._headers(AcceptType.JSON),
            create_time_map(
                coordinates,
                transportation,
                travel_time,
                time_info,
                search_range,
                level_of_detail,
                snapping,
                polygons_filter,
                remove_water_bodies,
                render_mode,
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
        snapping: Optional[Snapping] = None,
        polygons_filter: Optional[PolygonsFilter] = None,
        remove_water_bodies: Optional[bool] = None,
        render_mode: Optional[RenderMode] = None,
        v4_endpoint_path: Optional[str] = None,
    ) -> FeatureCollection:
        time_info = get_time_info(departure_time, arrival_time)

        resp = await send_post_async(
            FeatureCollection,
            v4_endpoint_path or "time-map",
            self._headers(AcceptType.GEO_JSON),
            create_time_map_geojson(
                coordinates,
                transportation,
                travel_time,
                time_info,
                search_range,
                level_of_detail,
                snapping,
                polygons_filter,
                remove_water_bodies,
                render_mode,
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
        snapping: Optional[Snapping] = None,
        polygons_filter: Optional[PolygonsFilter] = None,
        remove_water_bodies: Optional[bool] = None,
        render_mode: Optional[RenderMode] = None,
        v4_endpoint_path: Optional[str] = None,
    ) -> TimeMapWKTResponse:
        time_info = get_time_info(departure_time, arrival_time)

        resp = await send_post_async(
            TimeMapWKTResponse,
            v4_endpoint_path or "time-map",
            self._headers(AcceptType.WKT),
            create_time_map_wkt(
                coordinates,
                transportation,
                travel_time,
                time_info,
                search_range,
                level_of_detail,
                snapping,
                polygons_filter,
                remove_water_bodies,
                render_mode,
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
        snapping: Optional[Snapping] = None,
        polygons_filter: Optional[PolygonsFilter] = None,
        remove_water_bodies: Optional[bool] = None,
        render_mode: Optional[RenderMode] = None,
        v4_endpoint_path: Optional[str] = None,
    ) -> TimeMapWKTResponse:
        time_info = get_time_info(departure_time, arrival_time)

        resp = await send_post_async(
            TimeMapWKTResponse,
            v4_endpoint_path or "time-map",
            self._headers(AcceptType.WKT_NO_HOLES),
            create_time_map_wkt(
                coordinates,
                transportation,
                travel_time,
                time_info,
                search_range,
                level_of_detail,
                snapping,
                polygons_filter,
                remove_water_bodies,
                render_mode,
            ),
            self._sdk_params,
        )
        return resp

    async def h3_intersection_async(
        self,
        coordinates: List[Union[Coordinates, H3Centroid]],
        transportation: Union[
            PublicTransport,
            Driving,
            Ferry,
            Walking,
            Cycling,
            DrivingTrain,
            CyclingPublicTransport,
        ],
        resolution: int,
        properties: List[CellProperty] = [],
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        travel_time: int = 3600,
        search_range: Optional[Range] = None,
        snapping: Optional[Snapping] = None,
        v4_endpoint_path: Optional[str] = None,
    ) -> H3Result:
        time_info = get_time_info(departure_time, arrival_time)

        resp = await send_post_async(
            H3Response,
            v4_endpoint_path or "h3",
            self._headers(AcceptType.JSON),
            create_h3_intersection(
                coordinates=coordinates,
                transportation=transportation,
                resolution=resolution,
                properties=properties,
                travel_time=travel_time,
                time_info=time_info,
                search_range=search_range,
                snapping=snapping,
            ),
            self._sdk_params,
        )
        return resp.results[0]

    async def h3_union_async(
        self,
        coordinates: List[Union[Coordinates, H3Centroid]],
        transportation: Union[
            PublicTransport,
            Driving,
            Ferry,
            Walking,
            Cycling,
            DrivingTrain,
            CyclingPublicTransport,
        ],
        resolution: int,
        properties: List[CellProperty] = [],
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        travel_time: int = 3600,
        search_range: Optional[Range] = None,
        snapping: Optional[Snapping] = None,
        v4_endpoint_path: Optional[str] = None,
    ) -> H3Result:
        time_info = get_time_info(departure_time, arrival_time)

        resp = await send_post_async(
            H3Response,
            v4_endpoint_path or "h3",
            self._headers(AcceptType.JSON),
            create_h3_union(
                coordinates=coordinates,
                transportation=transportation,
                resolution=resolution,
                properties=properties,
                travel_time=travel_time,
                time_info=time_info,
                search_range=search_range,
                snapping=snapping,
            ),
            self._sdk_params,
        )

        return resp.results[0]

    async def h3_async(
        self,
        coordinates: List[Union[Coordinates, H3Centroid]],
        transportation: Union[
            PublicTransport,
            Driving,
            Ferry,
            Walking,
            Cycling,
            DrivingTrain,
            CyclingPublicTransport,
        ],
        resolution: int,
        properties: List[CellProperty] = [],
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        travel_time: int = 3600,
        search_range: Optional[Range] = None,
        snapping: Optional[Snapping] = None,
        v4_endpoint_path: Optional[str] = None,
    ) -> List[H3Result]:
        time_info = get_time_info(departure_time, arrival_time)

        resp = await send_post_async(
            H3Response,
            v4_endpoint_path or "h3",
            self._headers(AcceptType.JSON),
            create_h3(
                coordinates=coordinates,
                transportation=transportation,
                resolution=resolution,
                properties=properties,
                travel_time=travel_time,
                time_info=time_info,
                search_range=search_range,
                snapping=snapping,
            ),
            self._sdk_params,
        )
        return resp.results

    async def geohash_intersection_async(
        self,
        coordinates: List[Union[Coordinates, GeohashCentroid]],
        transportation: Union[
            PublicTransport,
            Driving,
            Ferry,
            Walking,
            Cycling,
            DrivingTrain,
            CyclingPublicTransport,
        ],
        resolution: int,
        properties: List[CellProperty] = [],
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        travel_time: int = 3600,
        search_range: Optional[Range] = None,
        snapping: Optional[Snapping] = None,
        v4_endpoint_path: Optional[str] = None,
    ) -> GeohashResult:
        time_info = get_time_info(departure_time, arrival_time)

        resp = await send_post_async(
            GeohashResponse,
            v4_endpoint_path or "geohash",
            self._headers(AcceptType.JSON),
            create_geohash_intersection(
                coordinates=coordinates,
                transportation=transportation,
                resolution=resolution,
                properties=properties,
                travel_time=travel_time,
                time_info=time_info,
                search_range=search_range,
                snapping=snapping,
            ),
            self._sdk_params,
        )
        return resp.results[0]

    async def geohash_union_async(
        self,
        coordinates: List[Union[Coordinates, GeohashCentroid]],
        transportation: Union[
            PublicTransport,
            Driving,
            Ferry,
            Walking,
            Cycling,
            DrivingTrain,
            CyclingPublicTransport,
        ],
        resolution: int,
        properties: List[CellProperty] = [],
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        travel_time: int = 3600,
        search_range: Optional[Range] = None,
        snapping: Optional[Snapping] = None,
        v4_endpoint_path: Optional[str] = None,
    ) -> GeohashResult:
        time_info = get_time_info(departure_time, arrival_time)

        resp = await send_post_async(
            GeohashResponse,
            v4_endpoint_path or "geohash",
            self._headers(AcceptType.JSON),
            create_geohash_union(
                coordinates=coordinates,
                transportation=transportation,
                resolution=resolution,
                properties=properties,
                travel_time=travel_time,
                time_info=time_info,
                search_range=search_range,
                snapping=snapping,
            ),
            self._sdk_params,
        )

        return resp.results[0]

    async def geohash_async(
        self,
        coordinates: List[Union[Coordinates, GeohashCentroid]],
        transportation: Union[
            PublicTransport,
            Driving,
            Ferry,
            Walking,
            Cycling,
            DrivingTrain,
            CyclingPublicTransport,
        ],
        resolution: int,
        properties: List[CellProperty] = [],
        departure_time: Optional[datetime] = None,
        arrival_time: Optional[datetime] = None,
        travel_time: int = 3600,
        search_range: Optional[Range] = None,
        snapping: Optional[Snapping] = None,
        v4_endpoint_path: Optional[str] = None,
    ) -> List[GeohashResult]:
        time_info = get_time_info(departure_time, arrival_time)

        resp = await send_post_async(
            GeohashResponse,
            v4_endpoint_path or "geohash",
            self._headers(AcceptType.JSON),
            create_geohash(
                coordinates=coordinates,
                transportation=transportation,
                resolution=resolution,
                properties=properties,
                travel_time=travel_time,
                time_info=time_info,
                search_range=search_range,
                snapping=snapping,
            ),
            self._sdk_params,
        )
        return resp.results

    async def distance_map_async(
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
        travel_distance: int = 900,
        level_of_detail: Optional[LevelOfDetail] = None,
        snapping: Optional[Snapping] = None,
        polygons_filter: Optional[PolygonsFilter] = None,
        no_holes: Optional[bool] = None,
        v4_endpoint_path: Optional[str] = None,
    ) -> List[TimeMapResult]:
        time_info = get_time_info(departure_time, arrival_time)
        resp = await send_post_async(
            TimeMapResponse,
            v4_endpoint_path or "distance-map",
            self._headers(AcceptType.JSON),
            create_distance_map(
                coordinates,
                transportation,
                travel_distance,
                time_info,
                level_of_detail,
                snapping,
                polygons_filter,
                no_holes,
            ),
            self._sdk_params,
        )
        return resp.results

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
            "User-Agent": self._user_agent,
            "Content-Type": "application/json",
            "Accept": accept_type.value,
        }


def get_time_info(departure_time: Optional[datetime], arrival_time: Optional[datetime]):
    if not departure_time and not arrival_time:
        raise ApiError("either arrival_time or departure_time has to be specified")

    if departure_time and arrival_time:
        raise ApiError("arrival_time and departure_time cannot be both specified")

    if departure_time:
        return DepartureTime(departure_time)
    elif arrival_time:
        return ArrivalTime(arrival_time)
