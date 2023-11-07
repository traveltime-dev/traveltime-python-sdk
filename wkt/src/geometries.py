from abc import ABC
from enum import Enum

from pydantic import BaseModel

from traveltimepy import Coordinates
from wkt.src.coordinates_models import (
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
