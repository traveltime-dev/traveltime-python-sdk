from typing import List, Union, Dict, Any, TypeVar, Iterator, Optional
from pydantic import BaseModel, Field, validator
from pydantic.generics import GenericModel

from traveltimepy.dto.responses.wkt_response_wrapper.src import WKTObject, parse_wkt

Props = TypeVar("Props", bound=Union[Dict[str, Any], BaseModel])


class TimeMapWKTResult(GenericModel):
    search_id: str
    shape: WKTObject
    properties: Optional[Props] = Field(None)

    @validator("shape", pre=True)
    def transform_shape(cls, shape: str) -> WKTObject:
        return parse_wkt(shape)


class TimeMapWKTResponse(BaseModel):
    results: List[TimeMapWKTResult]

    def __iter__(self) -> Iterator[TimeMapWKTResult]:
        return iter(self.results)

    def __len__(self) -> int:
        return len(self.results)

    def __getitem__(self, index: int) -> TimeMapWKTResult:
        return self.results[index]
