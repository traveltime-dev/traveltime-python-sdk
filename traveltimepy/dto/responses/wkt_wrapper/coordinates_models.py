from typing import List, Tuple
from pydantic import BaseModel

from traveltimepy import Coordinates


class LineStringCoordinates(BaseModel):
    coords: List[Coordinates]


class PolygonCoordinates(BaseModel):
    exterior: List[Coordinates]
    interiors: List[List[Coordinates]]


class MultiPointCoordinates(BaseModel):
    points: List[Coordinates]


class MultiLineStringCoordinates(BaseModel):
    lines: List[LineStringCoordinates]


class MultiPolygonCoordinates(BaseModel):
    polygons: List[PolygonCoordinates]
