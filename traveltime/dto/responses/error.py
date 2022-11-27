from pydantic.main import BaseModel


class ResponseError(BaseModel):
    error_code: int
    description: str
    documentation_link: str
