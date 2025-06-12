from typing import List, Optional

from geojson_pydantic import FeatureCollection

from traveltimepy.accept_type import AcceptType
from traveltimepy.async_base_client import AsyncBaseClient
from traveltimepy.requests.common import (
    Location,
    Rectangle,
    CellProperty,
    Coordinates,
)
from traveltimepy.requests.distance_map import (
    DistanceMapDepartureSearch,
    DistanceMapArrivalSearch,
    DistanceMapUnion,
    DistanceMapIntersection,
    DistanceMapRequest,
)
from traveltimepy.requests.geocoding import (
    GeocodingRequest,
    ReverseGeocodingRequest,
)
from traveltimepy.requests.geohash import (
    GeoHashDepartureSearch,
    GeoHashArrivalSearch,
    GeoHashUnion,
    GeoHashIntersection,
    GeoHashRequest,
)
from traveltimepy.requests.geohash_fast import (
    GeoHashFastArrivalSearches,
    GeoHashFastRequest,
)
from traveltimepy.requests.h3 import (
    H3DepartureSearch,
    H3ArrivalSearch,
    H3Union,
    H3Intersection,
    H3Request,
)
from traveltimepy.requests.h3_fast import H3FastRequest, H3FastArrivalSearches
from traveltimepy.requests.postcodes import (
    PostcodesRequest,
    PostcodeArrivalSearch,
    PostcodeDepartureSearch,
)
from traveltimepy.requests.postcodes_zones import (
    PostcodesDistrictsRequest,
    PostcodeFilterArrivalSearch,
    PostcodeFilterDepartureSearch,
    PostcodesSectorsRequest,
)
from traveltimepy.requests.routes import (
    RoutesArrivalSearch,
    RoutesDepartureSearch,
    RoutesRequest,
)
from traveltimepy.requests.supported_locations import SupportedLocationsRequest
from traveltimepy.requests.time_filter import (
    TimeFilterRequest,
    TimeFilterDepartureSearch,
    TimeFilterArrivalSearch,
)
from traveltimepy.requests.time_filter_fast import (
    TimeFilterFastArrivalSearches,
    TimeFilterFastRequest,
)
from traveltimepy.requests.time_filter_proto import (
    TimeFilterFastProtoRequest,
    TimeFilterFastProtoTransportation,
    RequestType,
    ProtoCountry,
)
from traveltimepy.requests.time_map import (
    TimeMapDepartureSearch,
    TimeMapArrivalSearch,
    TimeMapUnion,
    TimeMapIntersection,
    TimeMapRequest,
)
from traveltimepy.requests.time_map_fast import (
    TimeMapFastArrivalSearches,
    TimeMapFastRequest,
)
from traveltimepy.requests.time_map_fast_geojson import TimeMapFastGeojsonRequest
from traveltimepy.requests.time_map_fast_wkt import TimeMapFastWKTRequest
from traveltimepy.requests.time_map_geojson import TimeMapGeojsonRequest
from traveltimepy.requests.time_map_wkt import TimeMapWktRequest
from traveltimepy.responses.geohash import GeoHashResult, GeoHashResponse
from traveltimepy.responses.h3 import H3Result, H3Response
from traveltimepy.responses.map_info import MapInfoResponse, Map
from traveltimepy.responses.postcodes import PostcodesResponse, PostcodesResult
from traveltimepy.responses.routes import RoutesResult, RoutesResponse
from traveltimepy.responses.supported_locations import SupportedLocationsResponse
from traveltimepy.responses.time_filter import TimeFilterResponse, TimeFilterResult
from traveltimepy.responses.time_filter_fast import (
    TimeFilterFastResult,
    TimeFilterFastResponse,
)
from traveltimepy.responses.time_filter_proto import TimeFilterProtoResponse
from traveltimepy.responses.time_map import TimeMapResult, TimeMapResponse
from traveltimepy.responses.time_map_wkt import TimeMapWKTResponse
from traveltimepy.responses.zones import (
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
        resp: TimeFilterResponse = await self._api_call_post(
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
        resp: TimeFilterFastResponse = await self._api_call_post(
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
        res: MapInfoResponse = await self._api_call_get(
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
        """
        Match a query string to geographic coordinates using geocoding search.

        Converts addresses, postcodes, or venue names into geographic coordinates
        and location information. Supports filtering by country, bounding box.

        Args:
            query: A query to geocode. Can be an address, postcode, or venue name.
                   Examples: "SW1A 0AA", "Victoria street, London"
                   Including country/city improves accuracy.

            limit: Maximum number of results to return.
                   Must be between 1 and 50.

            within_countries: List of ISO 3166-1 alpha-2 or alpha-3 country codes
                             to limit results. Example: ["GB", "US"] or ["GBR", "USA"]

            format_name: If True, formats the name field to a well-formatted,
                        human-readable address. Experimental feature.

            format_exclude_country: If True, excludes country from the formatted name field.
                                   Only used when format_name is True.

            bounds: Geographic bounding box to limit search results.
                   Results will only include locations within this rectangle.

        Returns:
            FeatureCollection containing geocoding results with coordinates,
            addresses, confidence scores, and location metadata.
        """

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
        """
        Convert geographic coordinates to an address using reverse geocoding.

        Takes latitude and longitude coordinates and attempts to match them
        to the nearest address or location information.

        Args:
            lat: Latitude coordinate in decimal degrees.
                 Valid range: -90.0 to +90.0

            lng: Longitude coordinate in decimal degrees.
                 Valid range: -180.0 to +180.0

        Returns:
            FeatureCollection containing address information, confidence scores,
            and location metadata for the specified coordinates.

        Raises:
            400 Bad Request: If coordinates are far from land (e.g., in ocean).
                            Reverse search is only supported for points on land.

        Note:
            Results include formatted addresses, confidence scores indicating
            match quality, and metadata about transportation support for the area.
        """

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
        resp: SupportedLocationsResponse = await self._api_call_post(
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
        resp: TimeMapResponse = await self._api_call_post(
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
        resp: FeatureCollection = await self._api_call_post(
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
        resp: TimeMapWKTResponse = await self._api_call_post(
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
        resp: TimeMapWKTResponse = await self._api_call_post(
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
        resp: TimeMapResponse = await self._api_call_post(
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
        resp: FeatureCollection = await self._api_call_post(
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
        resp: TimeMapWKTResponse = await self._api_call_post(
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
        resp: TimeMapWKTResponse = await self._api_call_post(
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
        resp: H3Response = await self._api_call_post(
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
        resp: H3Response = await self._api_call_post(
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
    ) -> GeoHashResponse:
        """
        Calculate travel times to geohash cells within travel time catchment areas.

        Returns min, max, and mean travel times for each geohash cell. This is a more
        configurable version of geohash-fast but with lower performance.

        Args:
            arrival_searches: List of arrival-based searches calculating travel times
                             from geohash cells to specific destinations.

            departure_searches: List of departure-based searches calculating travel times
                               from specific origins to geohash cells.

            properties: List of travel time properties to calculate for each cell.
                       Options include minimum, maximum, and mean travel times.

            resolution: Geohash resolution of results to be returned.
                       Valid range: 1-6, where higher values provide more precise areas.

            unions: List of union operations combining multiple searches to show
                   total coverage across multiple access points.

            intersections: List of intersection operations finding cells that satisfy
                          multiple accessibility criteria simultaneously.

        Returns:
            GeoHashResponse containing travel time statistics for each geohash cell
            within the reachable area.

        Note:
            All search IDs must be unique across departure_searches, arrival_searches,
            unions, and intersections. Union and intersection operations reference
            search IDs from departure_searches and arrival_searches.
        """

        return await self._api_call_post(
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

    async def geohash_fast(
        self,
        arrival_searches: GeoHashFastArrivalSearches,
        properties: List[CellProperty],
        resolution: int,
    ) -> GeoHashResponse:
        """
        High-performance version of geohash search with fewer configurable parameters
        and more limited geographic coverage. Returns statistical travel time measures
        for each geohash cell.

        Args:
            arrival_searches: Arrival-based search configurations containing
                             many-to-one and one-to-many search definitions.

            properties: List of travel time properties to calculate for each cell.
                       Options include minimum, maximum, and mean travel times.

            resolution: Geohash resolution of results to be returned.
                       Valid range: 1-6, where higher values provide more precise areas.

        Returns:
            GeoHashResponse containing travel time statistics for each geohash cell
            within the reachable area.

        Note:
            This endpoint has limited geographic coverage compared to the standard
            geohash endpoint but offers significantly better performance.
        """
        return await self._api_call_post(
            GeoHashResponse,
            "geohash/fast",
            AcceptType.JSON,
            GeoHashFastRequest(
                resolution=resolution,
                properties=properties,
                arrival_searches=arrival_searches,
            ),
        )

    async def postcodes(
        self,
        arrival_searches: List[PostcodeArrivalSearch],
        departure_searches: List[PostcodeDepartureSearch],
    ) -> List[PostcodesResult]:
        resp: PostcodesResponse = await self._api_call_post(
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
        resp: PostcodesDistrictsResponse = await self._api_call_post(
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
        resp: PostcodesSectorsResponse = await self._api_call_post(
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
        resp: RoutesResponse = await self._api_call_post(
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
    ) -> TimeMapResponse:
        """
        Generate distance maps (isodistance polygons) showing areas reachable within specified travel distances.

        Creates polygon shapes representing all areas reachable within a travel distance limit
        from departure points or areas that can reach arrival points within distance constraints.
        Supports combining results through union and intersection operations.

        Args:
            arrival_searches: List of arrival-based searches showing areas that can reach
                             specific destinations within travel distance limits.

            departure_searches: List of departure-based searches showing areas reachable
                               from specific starting points within travel distance limits.

            unions: List of union operations combining multiple searches to show
                   total coverage areas across multiple access points.

            intersections: List of intersection operations finding areas that satisfy
                          multiple accessibility criteria simultaneously.

        Returns:
            TimeMapResponse containing polygon shapes for each search operation,
            with results sorted lexicographically by search_id.

        Note:
            All search IDs must be unique across departure_searches, arrival_searches,
            unions, and intersections. Union and intersection operations reference
            search IDs from departure_searches and arrival_searches.
        """

        return await self._api_call_post(
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
