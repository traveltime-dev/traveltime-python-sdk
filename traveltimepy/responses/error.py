from typing import Dict, List

from pydantic.main import BaseModel


class ResponseError(BaseModel):
    error_code: int
    description: str
    documentation_link: str
    additional_info: Dict[str, List[str]]
