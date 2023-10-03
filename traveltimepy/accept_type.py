from enum import Enum


class AcceptType(Enum):
    JSON = "application/json"
    WKT = "application/vnd.wkt+json"
    BOUNDING_BOXES_JSON = "application/vnd.bounding-boxes+json"
    GEO_JSON = "application/geo+json"
    OCTET_STREAM = "application/octet-stream"
