from typing import List
from fastkml import geometry, kml
from pydantic import BaseModel


class Placemark(BaseModel):
    name: str
    polygons: List[geometry.Polygon]

    class Config:
        arbitrary_types_allowed = True


class KMLResponse(BaseModel):
    placemarks: List[Placemark]


def parse_kml_as(kml_string: str) -> KMLResponse:
    k = kml.KML()
    kml_string_bytes = kml_string.encode("utf-8")
    k.from_string(kml_string_bytes)

    placemarks = (
        Placemark(name=placemark.name, polygons=list(placemark.geometry.geoms))
        for placemark in k.features()
    )

    return KMLResponse(placemarks=list(placemarks))
