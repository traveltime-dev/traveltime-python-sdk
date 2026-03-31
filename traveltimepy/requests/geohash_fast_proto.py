from enum import Enum
from typing import ClassVar, Optional, List, Union

try:
    import RequestsCommon_pb2  # type: ignore
    import GeohashFastRequest_pb2  # type: ignore

    PROTOBUF_AVAILABLE = True
except ImportError:
    PROTOBUF_AVAILABLE = False
    RequestsCommon_pb2 = None  # type: ignore
    GeohashFastRequest_pb2 = None  # type: ignore

from traveltimepy.requests.common import Coordinates
from traveltimepy.requests.time_filter_proto import (
    TransportationInfo,
    ProtoTransportation,
    ProtoPublicTransportWithDetails,
    ProtoDrivingAndPublicTransportWithDetails,
    RequestType,
    ProtoCountry,
)


class ProtoCellProperty(Enum):
    MEAN = 0
    MIN = 1
    MAX = 2


GeohashFastProtoTransportation = Union[
    ProtoTransportation,
    ProtoPublicTransportWithDetails,
    ProtoDrivingAndPublicTransportWithDetails,
]


class GeohashFastProtoRequest:
    originCoordinate: Coordinates
    transportation: GeohashFastProtoTransportation
    travelTime: int
    requestType: RequestType
    country: ProtoCountry
    resolution: int
    properties: List[ProtoCellProperty]

    def __init__(
        self,
        origin_coordinate: Coordinates,
        transportation: GeohashFastProtoTransportation,
        travel_time: int,
        request_type: RequestType,
        country: ProtoCountry,
        resolution: int,
        properties: List[ProtoCellProperty],
    ):
        self.originCoordinate = origin_coordinate
        self.transportation = transportation
        self.travelTime = travel_time
        self.requestType = request_type
        self.country = country
        self.resolution = resolution
        self.properties = properties

    def get_request(self) -> "GeohashFastRequest_pb2.GeohashFastRequest":  # type: ignore
        if not PROTOBUF_AVAILABLE:
            raise ImportError(
                "protobuf is required for GeohashFastProtoRequest. "
                "Install it with: pip install 'traveltimepy[proto]'"
            )
        request = GeohashFastRequest_pb2.GeohashFastRequest()  # type: ignore

        if self.requestType == RequestType.ONE_TO_MANY:
            req = request.oneToManyRequest
            req.departureLocation.lat = self.originCoordinate.lat
            req.departureLocation.lng = self.originCoordinate.lng
        else:
            req = request.manyToOneRequest
            req.arrivalLocation.lat = self.originCoordinate.lat
            req.arrivalLocation.lng = self.originCoordinate.lng

        # Set transportation type
        if isinstance(self.transportation, ProtoTransportation):
            req.transportation.type = self.transportation.value.code
        else:
            req.transportation.type = self.transportation.TYPE.value.code

            if isinstance(self.transportation, ProtoPublicTransportWithDetails):
                if self.transportation.walking_time_to_station is not None:
                    req.transportation.publicTransport.walkingTimeToStation.value = (
                        self.transportation.walking_time_to_station
                    )

            elif isinstance(
                self.transportation, ProtoDrivingAndPublicTransportWithDetails
            ):
                if self.transportation.walking_time_to_station is not None:
                    req.transportation.drivingAndPublicTransport.walkingTimeToStation.value = (
                        self.transportation.walking_time_to_station
                    )

                if self.transportation.driving_time_to_station is not None:
                    req.transportation.drivingAndPublicTransport.drivingTimeToStation.value = (
                        self.transportation.driving_time_to_station
                    )

                if self.transportation.parking_time is not None:
                    req.transportation.drivingAndPublicTransport.parkingTime.value = (
                        self.transportation.parking_time
                    )

        req.travelTime = self.travelTime
        req.arrivalTimePeriod = RequestsCommon_pb2.TimePeriod.WEEKDAY_MORNING  # type: ignore
        req.resolution = self.resolution

        for prop in self.properties:
            req.properties.append(prop.value)

        return request
