from enum import Enum


class RequestType(Enum):
    GET = 1
    POST = 2


class AcceptType(Enum):
    JSON = "application/json"
    BOUNDING_BOXES_JSON = "application/vnd.bounding-boxes+json"
    GEO_JSON = "application/geo+json"


