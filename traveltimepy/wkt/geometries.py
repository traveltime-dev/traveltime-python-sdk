from abc import ABC, abstractmethod
from enum import Enum
from typing import List

from pydantic import field_validator, BaseModel

from traveltimepy.requests.common import Coordinates
from traveltimepy.wkt.helper import print_indented


class GeometryType(Enum):
    POINT = "Point"
    LINESTRING = "LineString"
    POLYGON = "Polygon"
    MULTIPOINT = "MultiPoint"
    MULTILINESTRING = "MultiLineString"
    MULTIPOLYGON = "MultiPolygon"


class WKTObject(BaseModel, ABC):
    type: GeometryType

    @abstractmethod
    def pretty_print(self, indent_level=0):
        raise NotImplementedError("Subclasses must implement this method.")


class PointModel(WKTObject):
    coordinates: Coordinates

    def __init__(self, **data):
        super().__init__(type=GeometryType.POINT, **data)

    def pretty_print(self, indent_level=0):
        print_indented(
            f"POINT: {self.coordinates.lat}, {self.coordinates.lng}", indent_level
        )


class LineStringModel(WKTObject):
    coordinates: List[PointModel]

    def __init__(self, **data):
        super().__init__(type=GeometryType.LINESTRING, **data)

    @field_validator("coordinates")
    @classmethod
    def check_minimum_coordinates(cls, coords):
        if len(coords) < 2:
            raise ValueError("LineString must have at least 2 coordinates.")
        return coords

    def pretty_print(self, indent_level=0):
        print_indented("LINE STRING:", indent_level)
        for point in self.coordinates:
            point.pretty_print(indent_level + 1)


class PolygonModel(WKTObject):
    exterior: LineStringModel
    interiors: List[LineStringModel]

    def __init__(self, **data):
        super().__init__(type=GeometryType.POLYGON, **data)

    def pretty_print(self, indent_level=0):
        print_indented("POLYGON:", indent_level)
        print_indented("EXTERIOR:", indent_level + 1)
        self.exterior.pretty_print(indent_level + 2)
        if self.interiors:
            print_indented("INTERIORS:", indent_level + 1)
            for interior in self.interiors:
                interior.pretty_print(indent_level + 2)


class MultiPointModel(WKTObject):
    coordinates: List[PointModel]

    def __init__(self, **data):
        super().__init__(type=GeometryType.MULTIPOINT, **data)

    def pretty_print(self, indent_level=0):
        print_indented("MULTIPOINT:", indent_level)
        for point in self.coordinates:
            point.pretty_print(indent_level + 1)


class MultiLineStringModel(WKTObject):
    coordinates: List[LineStringModel]

    def __init__(self, **data):
        super().__init__(type=GeometryType.MULTILINESTRING, **data)

    def pretty_print(self, indent_level=0):
        print_indented("MULTILINESTRING:", indent_level)
        for linestring in self.coordinates:
            linestring.pretty_print(indent_level + 1)


class MultiPolygonModel(WKTObject):
    coordinates: List[PolygonModel]

    def __init__(self, **data):
        super().__init__(type=GeometryType.MULTIPOLYGON, **data)

    def pretty_print(self, indent_level=0):
        print_indented("MULTIPOLYGON:", indent_level)
        for polygon in self.coordinates:
            polygon.pretty_print(indent_level + 1)
