from typing import List, Union, Dict, Any, TypeVar, Iterator, Optional
from pydantic import BaseModel, Field, validator
from pydantic.generics import GenericModel
from enum import Enum

Props = TypeVar("Props", bound=Union[Dict[str, Any], BaseModel])


class WKTKeywords(Enum):
    POINT = "POINT"
    LINESTRING = "LINESTRING"
    POLYGON = "POLYGON"
    MULTIPOINT = "MULTIPOINT"
    MULTILINESTRING = "MULTILINESTRING"
    MULTIPOLYGON = "MULTIPOLYGON"
    GEOMETRYCOLLECTION = "GEOMETRYCOLLECTION"


class WKT(BaseModel):
    value: str = Field(..., description="WKT string representation of the geometry.")

    @validator("value", pre=True)
    def validate_wkt(cls, value: str) -> str:
        if not any(value.startswith(keyword.value) for keyword in WKTKeywords):
            raise ValueError(f"Invalid WKT: Must start with one of {', '.join([keyword.value for keyword in WKTKeywords])}")
        return value


class TimeMapWKTResult(GenericModel):
    search_id: str
    shape: WKT
    properties: Optional[Props] = Field(None)

    @validator("shape", pre=True)
    def transform_shape(cls, shape: str) -> Dict[str, str]:
        return {"value": shape}


class WKTResponseCollection(BaseModel):
    results: List[TimeMapWKTResult]

    def __iter__(self) -> Iterator[TimeMapWKTResult]:
        return iter(self.results)

    def __len__(self) -> int:
        return len(self.results)

    def __getitem__(self, index: int) -> TimeMapWKTResult:
        return self.results[index]
