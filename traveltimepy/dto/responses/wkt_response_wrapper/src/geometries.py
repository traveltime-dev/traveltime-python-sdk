from abc import ABC
from enum import Enum

from pydantic import BaseModel

from traveltimepy import Coordinates
from traveltimepy.dto.responses.wkt_response_wrapper.src.coordinates_models import (
    LineStringCoordinates,
    PolygonCoordinates,
    MultiPointCoordinates,
    MultiPolygonCoordinates,
    MultiLineStringCoordinates,
)


class GeometryType(Enum):
    POINT = "Point"
    LINESTRING = "LineString"
    POLYGON = "Polygon"
    MULTIPOINT = "MultiPoint"
    MULTILINESTRING = "MultiLineString"
    MULTIPOLYGON = "MultiPolygon"


class WKTObject(BaseModel, ABC):
    type: GeometryType

    def to_shapely(self):
        raise NotImplementedError("This method should be overridden by subclass")


class PointModel(WKTObject):
    coordinates: Coordinates


class LineStringModel(WKTObject):
    coordinates: LineStringCoordinates


class PolygonModel(WKTObject):
    coordinates: PolygonCoordinates


class MultiPointModel(WKTObject):
    coordinates: MultiPointCoordinates


class MultiLineStringModel(WKTObject):
    coordinates: MultiLineStringCoordinates


class MultiPolygonModel(WKTObject):
    coordinates: MultiPolygonCoordinates
