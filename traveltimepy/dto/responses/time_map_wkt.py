from typing import List, Union, Dict, Any, TypeVar, Optional
from pydantic import BaseModel, Field, validator
from pydantic.generics import GenericModel

from traveltimepy.wkt import WKTObject, parse_wkt
from traveltimepy.wkt.helper import print_indented

Props = TypeVar("Props", bound=Union[Dict[str, Any], BaseModel])


class TimeMapWKTResult(GenericModel):
    search_id: str
    shape: WKTObject
    properties: Optional[Props] = Field(None)

    @validator("shape", pre=True)
    def transform_shape(cls, shape: str) -> WKTObject:
        return parse_wkt(shape)

    def pretty_print(self, indent_level=0):
        print_indented(f"SEARCH ID: {self.search_id}", indent_level)
        self.shape.pretty_print(indent_level)
        print_indented(f"PROPERTIES: {self.properties}", indent_level)


class TimeMapWKTResponse(BaseModel):
    results: List[TimeMapWKTResult]

    def pretty_print(self, indent_level=0):
        print_indented("TIME-MAP WKT RESPONSE:", indent_level)
        for result in self.results:
            result.pretty_print(indent_level + 1)
            print()
