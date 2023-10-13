from enum import Enum


class AcceptType(Enum):
    JSON = "application/json"
    WKT = "application/vnd.wkt+json"
    WKT_NO_HOLES = "application/vnd.wkt-no-holes+json"
    BOUNDING_BOXES_JSON = "application/vnd.bounding-boxes+json"
    GEO_JSON = "application/geo+json"
    OCTET_STREAM = "application/octet-stream"
