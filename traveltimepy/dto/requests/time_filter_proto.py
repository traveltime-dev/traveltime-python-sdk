import math
from dataclasses import dataclass
from enum import Enum
from typing import List

from pydantic import BaseModel

from traveltimepy import TimeFilterFastRequest_pb2
from traveltimepy.dto import Coordinates


@dataclass
class TransportationInfo:
    code: int
    name: str


class Transportation(Enum):
    PUBLIC_TRANSPORT = TransportationInfo(0, 'pt')
    DRIVING = TransportationInfo(1, 'driving')
    DRIVING_FERRY = TransportationInfo(3, 'driving+ferry')
    WALKING = TransportationInfo(4, 'walking')
    CYCLING = TransportationInfo(5, 'cycling')
    CYCLING_FERRY = TransportationInfo(6, 'cycling+ferry')
    WALKING_FERRY = TransportationInfo(7, 'walking+ferry')


class Country(str, Enum):
    NETHERLANDS = 'nl'
    AUSTRIA = 'at'
    UNITED_KINGDOM = 'uk'
    BELGIUM = 'be'
    GERMANY = 'de'
    FRANCE = 'fr'
    IRELAND = 'ie'
    LITHUANIA = 'lt'


class OneToMany(BaseModel):
    origin_coordinates: Coordinates
    destination_coordinates: List[Coordinates]
    transportation: Transportation
    travel_time: int
    country: Country


class TimeFilterProtoRequest(BaseModel):
    one_to_many: OneToMany

    def to_proto(self) -> TimeFilterFastRequest_pb2.TimeFilterFastRequest:
        request = TimeFilterFastRequest_pb2.TimeFilterFastRequest()

        request.oneToManyRequest.departureLocation.lat = self.one_to_many.origin_coordinates.lat
        request.oneToManyRequest.departureLocation.lng = self.one_to_many.origin_coordinates.lng

        request.oneToManyRequest.transportation.type = self.one_to_many.transportation.value.code
        request.oneToManyRequest.travelTime = self.one_to_many.travel_time
        request.oneToManyRequest.arrivalTimePeriod = TimeFilterFastRequest_pb2.TimePeriod.WEEKDAY_MORNING

        mult = math.pow(10, 5)
        for destination in self.one_to_many.destination_coordinates:
            lat_delta = round((destination.lat - self.one_to_many.origin_coordinates.lat) * mult)
            lng_delta = round((destination.lng - self.one_to_many.origin_coordinates.lng) * mult)
            request.oneToManyRequest.locationDeltas.extend([lat_delta, lng_delta])

        return request
