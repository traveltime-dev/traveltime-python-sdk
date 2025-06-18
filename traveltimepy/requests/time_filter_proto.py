import math
from dataclasses import dataclass
from enum import Enum
from typing import ClassVar, Optional, List, Union

import RequestsCommon_pb2  # type: ignore
import TimeFilterFastRequest_pb2  # type: ignore
from traveltimepy.requests.common import Coordinates


class RequestType(Enum):
    # single departure location and multiple arrival locations
    ONE_TO_MANY = "one_to_many"
    # single arrival location and multiple departure locations
    MANY_TO_ONE = "many_to_one"


@dataclass
class TransportationInfo:
    code: int
    name: str


class ProtoTransportation(Enum):
    PUBLIC_TRANSPORT = TransportationInfo(0, "pt")
    DRIVING = TransportationInfo(1, "driving")
    DRIVING_AND_PUBLIC_TRANSPORT = TransportationInfo(2, "pt")
    DRIVING_FERRY = TransportationInfo(3, "driving+ferry")
    WALKING = TransportationInfo(4, "walking")
    CYCLING = TransportationInfo(5, "cycling")
    CYCLING_FERRY = TransportationInfo(6, "cycling+ferry")
    WALKING_FERRY = TransportationInfo(7, "walking+ferry")


@dataclass
class ProtoPublicTransportWithDetails:
    """Public transport configuration with detailed parameters.

    Attributes:
        walking_time_to_station: Limit on walking path duration. Must be > 0 and <= 1800.
    """

    walking_time_to_station: Optional[int] = None
    TYPE: ClassVar[ProtoTransportation] = ProtoTransportation.PUBLIC_TRANSPORT


@dataclass
class ProtoDrivingAndPublicTransportWithDetails:
    """Driving and public transport configuration with detailed parameters.

    Attributes:
        walking_time_to_station: Limit on walking path duration. Must be > 0 and <= 1800.
        driving_time_to_station: Limit on driving path duration. Must be > 0 and <= 1800.
        parking_time: Constant penalty to simulate finding a parking spot in seconds.
            Cannot be negative. Must be less than the overall travel time limit.
    """

    walking_time_to_station: Optional[int] = None
    driving_time_to_station: Optional[int] = None
    parking_time: Optional[int] = None
    TYPE: ClassVar[ProtoTransportation] = (
        ProtoTransportation.DRIVING_AND_PUBLIC_TRANSPORT
    )


TimeFilterFastProtoTransportation = Union[
    ProtoTransportation,
    ProtoPublicTransportWithDetails,
    ProtoDrivingAndPublicTransportWithDetails,
]


class ProtoCountry(str, Enum):
    NETHERLANDS = "nl"
    AUSTRIA = "at"
    UNITED_KINGDOM = "uk"
    BELGIUM = "be"
    GERMANY = "de"
    FRANCE = "fr"
    IRELAND = "ie"
    LITHUANIA = "lt"
    UNITED_STATES = "us"
    SOUTH_AFRICA = "za"
    ROMANIA = "ro"
    PORTUGAL = "pt"
    PHILIPPINES = "ph"
    NEW_ZEALAND = "nz"
    NORWAY = "no"
    LATVIA = "lv"
    JAPAN = "jp"
    INDIA = "in"
    INDONESIA = "id"
    HUNGARY = "hu"
    GREECE = "gr"
    FINLAND = "fi"
    DENMARK = "dk"
    CANADA = "ca"
    AUSTRALIA = "au"
    SINGAPORE = "sg"
    SWITZERLAND = "ch"
    SPAIN = "es"
    ITALY = "it"
    POLAND = "pl"
    SWEDEN = "se"
    LIECHTENSTEIN = "li"
    MEXICO = "mx"
    SAUDI_ARABIA = "sa"
    SERBIA = "rs"
    SLOVENIA = "si"


class TimeFilterFastProtoRequest:
    originCoordinate: Coordinates
    destinationCoordinates: List[Coordinates]
    transportation: TimeFilterFastProtoTransportation
    travelTime: int
    requestType: RequestType
    country: ProtoCountry
    withDistance: bool

    def __init__(
        self,
        origin_coordinate: Coordinates,
        destination_coordinates: List[Coordinates],
        transportation: TimeFilterFastProtoTransportation,
        travel_time: int,
        request_type: RequestType,
        country: ProtoCountry,
        with_distance: bool,
    ):
        self.originCoordinate = origin_coordinate
        self.destinationCoordinates = destination_coordinates
        self.transportation = transportation
        self.travelTime = travel_time
        self.requestType = request_type
        self.country = country
        self.withDistance = with_distance

    def get_request(self) -> TimeFilterFastRequest_pb2.TimeFilterFastRequest:  # type: ignore
        request = TimeFilterFastRequest_pb2.TimeFilterFastRequest()  # type: ignore

        if self.requestType.ONE_TO_MANY:
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
        else:  # PublicTransportDetails or DrivingAndPublicTransportDetails
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

        if self.withDistance:
            req.properties.extend(
                [TimeFilterFastRequest_pb2.TimeFilterFastRequest.Property.DISTANCES]  # type: ignore
            )

        # Calculate and add location deltas
        mult = math.pow(10, 5)
        for destination in self.destinationCoordinates:
            lat_delta = round((destination.lat - self.originCoordinate.lat) * mult)
            lng_delta = round((destination.lng - self.originCoordinate.lng) * mult)
            req.locationDeltas.extend([lat_delta, lng_delta])

        return request
