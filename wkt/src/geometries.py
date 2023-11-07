from abc import ABC
from enum import Enum
from typing import List

from pydantic import BaseModel

from traveltimepy import Coordinates


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
    coordinates: List[PointModel]


class PolygonModel(WKTObject):
    exterior: LineStringModel
    interiors: List[LineStringModel]


class MultiPointModel(WKTObject):
    coordinates: List[PointModel]


class MultiLineStringModel(WKTObject):
    coordinates: List[LineStringModel]


class MultiPolygonModel(WKTObject):
    coordinates: List[PolygonModel]
