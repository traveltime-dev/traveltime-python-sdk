from typing import Optional, List

from pydantic import BaseModel

from traveltimepy.requests.common import Rectangle
from traveltimepy.itertools import join_opt


class GeocodingRequest(BaseModel):
    query: str
    limit: Optional[int] = None
    within_countries: Optional[List[str]] = None
    format_name: Optional[bool] = None
    format_exclude_country: Optional[bool] = None
    bounds: Optional[Rectangle] = None

    def get_params(self):
        full_query = {
            "query": self.query,
            "limit": self.limit,
            "within.country": join_opt(self.within_countries, ","),
            "format.name": self.format_name,
            "format.exclude.country": self.format_exclude_country,
            "bounds": self.bounds.to_str() if self.bounds is not None else self.bounds,
        }
        return {
            key: str(value) for (key, value) in full_query.items() if value is not None
        }


class ReverseGeocodingRequest(BaseModel):
    lat: float
    lng: float

    def get_params(self):
        full_query = {"lat": self.lat, "lng": self.lng}
        return {
            key: str(value) for (key, value) in full_query.items() if value is not None
        }
