class InvalidWKTStringError(Exception):
    def __init__(self, wkt_str):
        super().__init__(f"Invalid WKT string: {wkt_str}")


class InvalidFunctionError(Exception):
    def __init__(self, geometry):
        super().__init__(f"No function found for geometry type: {type(geometry)}")


class InvalidGeometryTypeError(Exception):
    def __init__(self, geometry):
        super().__init__(f"Invalid or unsupported geometry type: {type(geometry)}")


class NullGeometryError(Exception):
    def __init__(self):
        super().__init__("Null, undefined or empty geometry returned")
