from typing import List, Optional
from fastkml import KML, Placemark, kml
from pydantic import BaseModel

# The stable version of fastkml is from 2021 and does not have types defined, nor
# a `py.typed` file. There are newer pre-release versions as new as 2024, but they
# seem to be undoccumented.
# TODO: Maybe port this into newer versions of fastkml for proper type checking support


class TimeMapKmlResult(BaseModel):
    placemark: Placemark

    def search_id(self) -> str:
        return self.placemark.name  # type: ignore

    def pretty_string(self) -> str:  # type: ignore
        return self.placemark.to_string(prettyprint=True)

    class Config:
        arbitrary_types_allowed = True


class TimeMapKmlResponse(BaseModel):
    results: List[TimeMapKmlResult]


def parse_kml_as(kml_string: str) -> TimeMapKmlResponse:
    k = kml.KML()
    k.from_string(kml_string.encode("utf-8"))

    results = [
        TimeMapKmlResult(placemark=feature)
        for feature in k.features()
        if isinstance(feature, kml.Placemark)
    ]

    return TimeMapKmlResponse(results=results)
