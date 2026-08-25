from typing import List, Optional, Union

try:
    from traveltimepy.proto import RequestsCommon_pb2  # type: ignore
    from traveltimepy.proto import H3FastRequest_pb2  # type: ignore

    PROTOBUF_AVAILABLE = True
except ImportError:
    PROTOBUF_AVAILABLE = False
    RequestsCommon_pb2 = None  # type: ignore
    H3FastRequest_pb2 = None  # type: ignore

from traveltimepy.requests.common import Coordinates
from traveltimepy.requests.geohash_fast_proto import ProtoCellProperty
from traveltimepy.requests.time_filter_proto import (
    ProtoTransportation,
    ProtoPublicTransportWithDetails,
    ProtoDrivingAndPublicTransportWithDetails,
    RequestType,
    ProtoCountry,
)

H3FastProtoTransportation = Union[
    ProtoTransportation,
    ProtoPublicTransportWithDetails,
    ProtoDrivingAndPublicTransportWithDetails,
]


class H3FastProtoRequest:
    originCoordinate: Coordinates
    transportation: H3FastProtoTransportation
    travelTime: int
    requestType: RequestType
    country: ProtoCountry
    resolution: int
    properties: List[ProtoCellProperty]
    removeWaterBodies: Optional[bool]

    def __init__(
        self,
        origin_coordinate: Coordinates,
        transportation: H3FastProtoTransportation,
        travel_time: int,
        request_type: RequestType,
        country: ProtoCountry,
        resolution: int,
        properties: List[ProtoCellProperty],
        remove_water_bodies: Optional[bool] = None,
    ):
        self.originCoordinate = origin_coordinate
        self.transportation = transportation
        self.travelTime = travel_time
        self.requestType = request_type
        self.country = country
        self.resolution = resolution
        self.properties = properties
        self.removeWaterBodies = remove_water_bodies

    def get_request(self) -> "H3FastRequest_pb2.H3FastRequest":  # type: ignore
        if not PROTOBUF_AVAILABLE:
            raise ImportError(
                "protobuf is required for H3FastProtoRequest. "
                "Install it with: pip install 'traveltimepy[proto]'"
            )
        request = H3FastRequest_pb2.H3FastRequest()  # type: ignore

        if self.requestType == RequestType.ONE_TO_MANY:
            req = request.oneToManyRequest
            req.departureLocation.lat = self.originCoordinate.lat
            req.departureLocation.lng = self.originCoordinate.lng
        else:
            req = request.manyToOneRequest
            req.arrivalLocation.lat = self.originCoordinate.lat
            req.arrivalLocation.lng = self.originCoordinate.lng

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
        if self.removeWaterBodies is not None:
            req.removeWaterBodies = self.removeWaterBodies

        for prop in self.properties:
            req.properties.append(prop.value)

        return request
