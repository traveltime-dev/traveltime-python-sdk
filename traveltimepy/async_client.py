from typing import List, Optional

from geojson_pydantic import FeatureCollection

from traveltimepy.accept_type import AcceptType
from traveltimepy.async_base_client import AsyncBaseClient
from traveltimepy.dto.common import (
    Location, Rectangle,
)
from traveltimepy.dto.requests.geocoding import GeocodingRequest, ReverseGeocodingRequest
from traveltimepy.dto.requests.time_filter import TimeFilterRequest, TimeFilterDepartureSearch, TimeFilterArrivalSearch
from traveltimepy.dto.responses.map_info import MapInfoResponse, Map
from traveltimepy.dto.responses.time_filter import TimeFilterResponse, TimeFilterResult


class AsyncClient(AsyncBaseClient):

    async def time_filter(
        self,
        locations: List[Location],
        departure_searches: List[TimeFilterDepartureSearch],
        arrival_searches: List[TimeFilterArrivalSearch]
    ) -> List[TimeFilterResult]:
        resp = await self._api_call_post(
            TimeFilterResponse,
            "time-filter",
            AcceptType.JSON,
            TimeFilterRequest(
                locations=locations,
                departure_searches=departure_searches,
                arrival_searches=arrival_searches
            )
        )

        return resp.results

    async def map_info(
        self
    ) -> List[Map]:
        res = await self._api_call_get(
            MapInfoResponse,
            "map-info",
            AcceptType.JSON,
            None
        )
        return res.maps

    async def geocoding(
        self,
        query: str,
        limit: Optional[int] = None,
        within_countries: Optional[List[str]] = None,
        format_name: Optional[bool] = None,
        format_exclude_country: Optional[bool] = None,
        bounds: Optional[Rectangle] = None
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
                bounds=bounds
            ).get_params()
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
            ReverseGeocodingRequest(lat=lat, lng=lng).get_params()
        )

