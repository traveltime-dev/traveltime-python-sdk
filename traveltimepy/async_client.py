from typing import List, Optional

from geojson_pydantic import FeatureCollection

from traveltimepy.accept_type import AcceptType
from traveltimepy.async_base_client import AsyncBaseClient
from traveltimepy.dto.common import (
    Location,
    Rectangle,
    CellProperty,
    Coordinates,
)
from traveltimepy.dto.requests.distance_map import (
    DistanceMapDepartureSearch,
    DistanceMapArrivalSearch,
    DistanceMapUnion,
    DistanceMapIntersection,
    DistanceMapRequest,
)
from traveltimepy.dto.requests.geocoding import (
    GeocodingRequest,
    ReverseGeocodingRequest,
)
from traveltimepy.dto.requests.geohash import (
    GeoHashDepartureSearch,
    GeoHashArrivalSearch,
    GeoHashUnion,
    GeoHashIntersection,
    GeoHashRequest,
)
from traveltimepy.dto.requests.geohash_fast import (
    GeoHashFastArrivalSearches,
    GeoHashFastRequest,
)
from traveltimepy.dto.requests.h3 import (
    H3DepartureSearch,
    H3ArrivalSearch,
    H3Union,
    H3Intersection,
    H3Request,
)
from traveltimepy.dto.requests.h3_fast import H3FastRequest, H3FastArrivalSearches
from traveltimepy.dto.requests.postcodes import (
    PostcodesRequest,
    PostcodeArrivalSearch,
    PostcodeDepartureSearch,
)
from traveltimepy.dto.requests.postcodes_zones import (
    PostcodesDistrictsRequest,
    PostcodeFilterArrivalSearch,
    PostcodeFilterDepartureSearch,
    PostcodesSectorsRequest,
)
from traveltimepy.dto.requests.routes import (
    RoutesArrivalSearch,
    RoutesDepartureSearch,
    RoutesRequest,
)
from traveltimepy.dto.requests.supported_locations import SupportedLocationsRequest
from traveltimepy.dto.requests.time_filter import (
    TimeFilterRequest,
    TimeFilterDepartureSearch,
    TimeFilterArrivalSearch,
)
from traveltimepy.dto.requests.time_filter_fast import (
    TimeFilterFastArrivalSearches,
    TimeFilterFastRequest,
)
from traveltimepy.dto.requests.time_filter_proto import (
    TimeFilterFastProtoRequest,
    TimeFilterFastProtoTransportation,
    RequestType,
    ProtoCountry,
)
from traveltimepy.dto.requests.time_map import (
    TimeMapDepartureSearch,
    TimeMapArrivalSearch,
    TimeMapUnion,
    TimeMapIntersection,
    TimeMapRequest,
)
from traveltimepy.dto.requests.time_map_fast import (
    TimeMapFastArrivalSearches,
    TimeMapFastRequest,
)
from traveltimepy.dto.requests.time_map_fast_geojson import TimeMapFastGeojsonRequest
from traveltimepy.dto.requests.time_map_fast_wkt import TimeMapFastWKTRequest
from traveltimepy.dto.requests.time_map_geojson import TimeMapGeojsonRequest
from traveltimepy.dto.requests.time_map_wkt import TimeMapWktRequest
from traveltimepy.dto.responses.geohash import GeoHashResult, GeoHashResponse
from traveltimepy.dto.responses.h3 import H3Result, H3Response
from traveltimepy.dto.responses.map_info import MapInfoResponse, Map
from traveltimepy.dto.responses.postcodes import PostcodesResponse, PostcodesResult
from traveltimepy.dto.responses.routes import RoutesResult, RoutesResponse
from traveltimepy.dto.responses.supported_locations import SupportedLocationsResponse
from traveltimepy.dto.responses.time_filter import TimeFilterResponse, TimeFilterResult
from traveltimepy.dto.responses.time_filter_fast import (
    TimeFilterFastResult,
    TimeFilterFastResponse,
)
from traveltimepy.dto.responses.time_filter_proto import TimeFilterProtoResponse
from traveltimepy.dto.responses.time_map import TimeMapResult, TimeMapResponse
from traveltimepy.dto.responses.time_map_wkt import TimeMapWKTResponse
from traveltimepy.dto.responses.zones import (
    PostcodesDistrictsResult,
    PostcodesDistrictsResponse,
    PostcodesSectorsResult,
    PostcodesSectorsResponse,
)


class AsyncClient(AsyncBaseClient):

    async def time_filter(
        self,
        locations: List[Location],
        departure_searches: List[TimeFilterDepartureSearch],
        arrival_searches: List[TimeFilterArrivalSearch],
    ) -> List[TimeFilterResult]:
        resp = await self._api_call_post(
            TimeFilterResponse,
            "time-filter",
            AcceptType.JSON,
            TimeFilterRequest(
                locations=locations,
                departure_searches=departure_searches,
                arrival_searches=arrival_searches,
            ),
        )
        return resp.results

    async def time_filter_fast(
        self, locations: List[Location], arrival_searches: TimeFilterFastArrivalSearches
    ) -> List[TimeFilterFastResult]:
        resp = await self._api_call_post(
            TimeFilterFastResponse,
            "time-filter/fast",
            AcceptType.JSON,
            TimeFilterFastRequest(
                locations=locations, arrival_searches=arrival_searches
            ),
        )
        return resp.results

    async def time_filter_proto(
        self,
        origin_coordinate: Coordinates,
        destination_coordinates: List[Coordinates],
        transportation: TimeFilterFastProtoTransportation,
        travel_time: int,
        request_type: RequestType,
        country: ProtoCountry,
        with_distance: bool,
    ) -> TimeFilterProtoResponse:
        return await self._api_call_proto(
            TimeFilterFastProtoRequest(
                origin_coordinate,
                destination_coordinates,
                transportation,
                travel_time,
                request_type,
                country,
                with_distance,
            )
        )

    async def map_info(self) -> List[Map]:
        res = await self._api_call_get(
            MapInfoResponse, "map-info", AcceptType.JSON, None
        )
        return res.maps

    async def geocoding(
        self,
        query: str,
        limit: Optional[int] = None,
        within_countries: Optional[List[str]] = None,
        format_name: Optional[bool] = None,
        format_exclude_country: Optional[bool] = None,
        bounds: Optional[Rectangle] = None,
    ) -> FeatureCollection:
        return await self._api_call_get(
            FeatureCollection,
            "geocoding/search",
            AcceptType.JSON,
            GeocodingRequest(
                query=query,
                limit=limit,
                within_countries=within_countries,
                format_name=format_name,
                format_exclude_country=format_exclude_country,
                bounds=bounds,
            ).get_params(),
        )

    async def reverse_geocoding(
        self,
        lat: float,
        lng: float,
    ) -> FeatureCollection:
        return await self._api_call_get(
            FeatureCollection,
            "geocoding/reverse",
            AcceptType.JSON,
            ReverseGeocodingRequest(lat=lat, lng=lng).get_params(),
        )

    async def supported_locations(
        self,
        locations: List[Location],
    ) -> SupportedLocationsResponse:
        resp = await self._api_call_post(
            SupportedLocationsResponse,
            "supported-locations",
            AcceptType.JSON,
            SupportedLocationsRequest(locations=locations),
        )
        return resp

    async def time_map(
        self,
        arrival_searches: List[TimeMapArrivalSearch],
        departure_searches: List[TimeMapDepartureSearch],
        unions: List[TimeMapUnion],
        intersections: List[TimeMapIntersection],
    ) -> List[TimeMapResult]:
        resp = await self._api_call_post(
            TimeMapResponse,
            "time-map",
            AcceptType.JSON,
            TimeMapRequest(
                arrival_searches=arrival_searches,
                departure_searches=departure_searches,
                unions=unions,
                intersections=intersections,
            ),
        )
        return resp.results

    async def time_map_geojson(
        self,
        arrival_searches: List[TimeMapArrivalSearch],
        departure_searches: List[TimeMapDepartureSearch],
    ) -> FeatureCollection:
        resp = await self._api_call_post(
            FeatureCollection,
            "time-map",
            AcceptType.GEO_JSON,
            TimeMapGeojsonRequest(
                arrival_searches=arrival_searches, departure_searches=departure_searches
            ),
        )
        return resp

    async def time_map_wkt(
        self,
        arrival_searches: List[TimeMapArrivalSearch],
        departure_searches: List[TimeMapDepartureSearch],
    ) -> TimeMapWKTResponse:
        resp = await self._api_call_post(
            TimeMapWKTResponse,
            "time-map",
            AcceptType.WKT,
            TimeMapWktRequest(
                arrival_searches=arrival_searches, departure_searches=departure_searches
            ),
        )
        return resp

    async def time_map_wkt_no_holes(
        self,
        arrival_searches: List[TimeMapArrivalSearch],
        departure_searches: List[TimeMapDepartureSearch],
    ) -> TimeMapWKTResponse:
        resp = await self._api_call_post(
            TimeMapWKTResponse,
            "time-map",
            AcceptType.WKT_NO_HOLES,
            TimeMapWktRequest(
                arrival_searches=arrival_searches, departure_searches=departure_searches
            ),
        )
        return resp

    async def time_map_fast(
        self,
        arrival_searches: TimeMapFastArrivalSearches,
    ) -> List[TimeMapResult]:
        resp = await self._api_call_post(
            TimeMapResponse,
            "time-map/fast",
            AcceptType.JSON,
            TimeMapFastRequest(arrival_searches=arrival_searches),
        )
        return resp.results

    async def time_map_fast_geojson(
        self,
        arrival_searches: TimeMapFastArrivalSearches,
    ) -> FeatureCollection:
        resp = await self._api_call_post(
            FeatureCollection,
            "time-map/fast",
            AcceptType.GEO_JSON,
            TimeMapFastGeojsonRequest(arrival_searches=arrival_searches),
        )
        return resp

    async def time_map_fast_wkt(
        self,
        arrival_searches: TimeMapFastArrivalSearches,
    ) -> TimeMapWKTResponse:
        resp = await self._api_call_post(
            TimeMapWKTResponse,
            "time-map/fast",
            AcceptType.WKT,
            TimeMapFastWKTRequest(arrival_searches=arrival_searches),
        )
        return resp

    async def time_map_fast_wkt_no_holes(
        self,
        arrival_searches: TimeMapFastArrivalSearches,
    ) -> TimeMapWKTResponse:
        resp = await self._api_call_post(
            TimeMapWKTResponse,
            "time-map/fast",
            AcceptType.WKT_NO_HOLES,
            TimeMapFastWKTRequest(arrival_searches=arrival_searches),
        )
        return resp

    async def h3(
        self,
        arrival_searches: List[H3ArrivalSearch],
        departure_searches: List[H3DepartureSearch],
        properties: List[CellProperty],
        resolution: int,
        unions: List[H3Union],
        intersections: List[H3Intersection],
    ) -> List[H3Result]:
        resp = await self._api_call_post(
            H3Response,
            "h3",
            AcceptType.JSON,
            H3Request(
                resolution=resolution,
                properties=properties,
                departure_searches=departure_searches,
                arrival_searches=arrival_searches,
                unions=unions,
                intersections=intersections,
            ),
        )
        return resp.results

    async def h3_fast(
        self,
        arrival_searches: H3FastArrivalSearches,
        properties: List[CellProperty],
        resolution: int,
    ) -> List[H3Result]:
        resp = await self._api_call_post(
            H3Response,
            "h3/fast",
            AcceptType.JSON,
            H3FastRequest(
                resolution=resolution,
                properties=properties,
                arrival_searches=arrival_searches,
            ),
        )
        return resp.results

    async def geohash(
        self,
        arrival_searches: List[GeoHashArrivalSearch],
        departure_searches: List[GeoHashDepartureSearch],
        properties: List[CellProperty],
        resolution: int,
        unions: List[GeoHashUnion],
        intersections: List[GeoHashIntersection],
    ) -> List[GeoHashResult]:
        resp = await self._api_call_post(
            GeoHashResponse,
            "geohash",
            AcceptType.JSON,
            GeoHashRequest(
                resolution=resolution,
                properties=properties,
                departure_searches=departure_searches,
                arrival_searches=arrival_searches,
                unions=unions,
                intersections=intersections,
            ),
        )
        return resp.results

    async def geohash_fast(
        self,
        arrival_searches: GeoHashFastArrivalSearches,
        properties: List[CellProperty],
        resolution: int,
    ) -> List[GeoHashResult]:
        resp = await self._api_call_post(
            GeoHashResponse,
            "geohash/fast",
            AcceptType.JSON,
            GeoHashFastRequest(
                resolution=resolution,
                properties=properties,
                arrival_searches=arrival_searches,
            ),
        )
        return resp.results

    async def postcodes(
        self,
        arrival_searches: List[PostcodeArrivalSearch],
        departure_searches: List[PostcodeDepartureSearch],
    ) -> List[PostcodesResult]:
        resp = await self._api_call_post(
            PostcodesResponse,
            "time-filter/postcodes",
            AcceptType.JSON,
            PostcodesRequest(
                arrival_searches=arrival_searches, departure_searches=departure_searches
            ),
        )
        return resp.results

    async def postcode_districts(
        self,
        arrival_searches: List[PostcodeFilterArrivalSearch],
        departure_searches: List[PostcodeFilterDepartureSearch],
    ) -> List[PostcodesDistrictsResult]:
        resp = await self._api_call_post(
            PostcodesDistrictsResponse,
            "time-filter/postcode-districts",
            AcceptType.JSON,
            PostcodesDistrictsRequest(
                arrival_searches=arrival_searches, departure_searches=departure_searches
            ),
        )
        return resp.results

    async def postcode_sectors(
        self,
        arrival_searches: List[PostcodeFilterArrivalSearch],
        departure_searches: List[PostcodeFilterDepartureSearch],
    ) -> List[PostcodesSectorsResult]:
        resp = await self._api_call_post(
            PostcodesSectorsResponse,
            "time-filter/postcode-sectors",
            AcceptType.JSON,
            PostcodesSectorsRequest(
                arrival_searches=arrival_searches, departure_searches=departure_searches
            ),
        )
        return resp.results

    async def routes(
        self,
        locations: List[Location],
        arrival_searches: List[RoutesArrivalSearch],
        departure_searches: List[RoutesDepartureSearch],
    ) -> List[RoutesResult]:
        resp = await self._api_call_post(
            RoutesResponse,
            "routes",
            AcceptType.JSON,
            RoutesRequest(
                locations=locations,
                departure_searches=departure_searches,
                arrival_searches=arrival_searches,
            ),
        )
        return resp.results

    async def distance_map(
        self,
        arrival_searches: List[DistanceMapArrivalSearch],
        departure_searches: List[DistanceMapDepartureSearch],
        unions: List[DistanceMapUnion],
        intersections: List[DistanceMapIntersection],
    ) -> List[TimeMapResult]:
        resp = await self._api_call_post(
            TimeMapResponse,
            "distance-map",
            AcceptType.JSON,
            DistanceMapRequest(
                departure_searches=departure_searches,
                arrival_searches=arrival_searches,
                unions=unions,
                intersections=intersections,
            ),
        )
        return resp.results
