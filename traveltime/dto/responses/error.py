from dataclasses import dataclass


@dataclass(frozen=True)
class ResponseError:
    error_code: int
    description: str
    documentation_link: str
