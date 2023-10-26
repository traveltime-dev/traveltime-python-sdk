from abc import ABC

from pydantic import BaseModel
from shapely.geometry import (
    Point,
    LineString,
    Polygon,
    MultiPoint,
    MultiLineString,
    MultiPolygon,
)


class WKTObject(BaseModel, ABC):
    type: str
    coordinates: list

    def to_shapely(self):
        raise NotImplementedError("This method should be overridden by subclass")


class PointModel(WKTObject):
    def to_shapely(self):
        assert self.type == "Point"
        return Point(self.coordinates)


class LineStringModel(WKTObject):
    def to_shapely(self):
        assert self.type == "LineString"
        return LineString(self.coordinates)


class PolygonModel(WKTObject):
    def to_shapely(self):
        assert self.type == "Polygon"
        return Polygon(self.coordinates[0], self.coordinates[1:])


class MultiPointModel(WKTObject):
    def to_shapely(self):
        assert self.type == "MultiPoint"
        return MultiPoint(self.coordinates)


class MultiLineStringModel(WKTObject):
    def to_shapely(self):
        assert self.type == "MultiLineString"
        return MultiLineString(self.coordinates)


class MultiPolygonModel(WKTObject):
    def to_shapely(self):
        assert self.type == "MultiPolygon"
        return MultiPolygon([Polygon(p[0], p[1:]) for p in self.coordinates])
