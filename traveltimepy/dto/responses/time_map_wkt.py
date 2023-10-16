from typing import List, Union, Dict, Any, TypeVar, Iterator, Optional
from pydantic import BaseModel, Field, validator
from pydantic.generics import GenericModel
from shapely import wkt
from shapely.errors import WKTReadingError

Props = TypeVar("Props", bound=Union[Dict[str, Any], BaseModel])


class WKT(BaseModel):
    value: str = Field(..., description="WKT string representation of the geometry.")

    @validator("value", pre=True)
    def validate_wkt(cls, value: str) -> str:
        try:
            wkt.loads(value)
            return value
        except WKTReadingError:
            raise ValueError("Invalid WKT string")


class TimeMapWKTResult(GenericModel):
    search_id: str
    shape: WKT
    properties: Optional[Props] = Field(None)

    @validator("shape", pre=True)
    def transform_shape(cls, shape: str) -> Dict[str, str]:
        return {"value": shape}

    # Used for getting json format response
    #
    # Example:
    # results_dicts = [result.dict() for result in results]
    # results_json_str = json.dumps(results_dicts)
    # print(results_json_str)
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
