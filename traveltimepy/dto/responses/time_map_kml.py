from typing import List
from fastkml import geometry, kml
from pydantic import BaseModel


class Placemark(BaseModel):
    name: str
    polygons: List[geometry.Polygon]

    class Config:
        arbitrary_types_allowed = True


class TimeMapKmlResponse(BaseModel):
    placemarks: List[Placemark]

    def to_fastkml(self) -> kml.KML:
        k = kml.KML()
        doc = kml.Document()
        k.append(doc)

        for placemark_data in self.placemarks:
            pm = kml.Placemark()
            pm.name = placemark_data.name
            pm.geometry = geometry.MultiPolygon(polygons=placemark_data.polygons)
            doc.append(pm)

        return k


def parse_kml_as(kml_string: str) -> TimeMapKmlResponse:
    k = kml.KML()
    kml_string_bytes = kml_string.encode("utf-8")
    k.from_string(kml_string_bytes)

    placemarks = (
        Placemark(name=placemark.name, polygons=list(placemark.geometry.geoms))
        for placemark in k.features()
    )

    return TimeMapKmlResponse(placemarks=list(placemarks))
