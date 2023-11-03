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

    placemarks = []
    for placemark in k.features():
        polygons = list(placemark.geometry.geoms)
        placemarks.append(Placemark(name=placemark.name, polygons=polygons))

    # Create and return a KMLResponse instance
    return KMLResponse(placemarks=placemarks)
