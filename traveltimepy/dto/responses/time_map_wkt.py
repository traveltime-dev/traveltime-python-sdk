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
        valid_keywords = [keyword.value for keyword in WKTKeywords]
        if not any(value.startswith(keyword) for keyword in valid_keywords):
            raise ValueError(
                f"Invalid WKT: Must start with one of "
                f"{', '.join(valid_keywords)}"
            )
        return value


class TimeMapWKTResult(GenericModel):
    search_id: str
    shape: WKT
    properties: Optional[Props] = Field(None)

    @validator("shape", pre=True)
    def transform_shape(cls, shape: str) -> Dict[str, str]:
        return {"value": shape}

    def dict(self, **kwargs):
        original_dict = super().dict(**kwargs)
        original_dict['shape'] = original_dict['shape']['value']
        return original_dict


class WKTResponseCollection(BaseModel):
    results: List[TimeMapWKTResult]

    def __iter__(self) -> Iterator[TimeMapWKTResult]:
        return iter(self.results)

    def __len__(self) -> int:
        return len(self.results)

    def __getitem__(self, index: int) -> TimeMapWKTResult:
        return self.results[index]
