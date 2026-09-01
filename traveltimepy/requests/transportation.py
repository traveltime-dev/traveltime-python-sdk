from enum import Enum
from typing import List, Literal, Optional

from pydantic.main import BaseModel
from pydantic import model_validator

from traveltimepy.requests.common import DrivingTrafficModel


class MaxChanges(BaseModel):
    enabled: bool
    limit: int


class IncludeRoads(str, Enum):
    """Additional road types to include when executing a search.

    By default all of these roads are excluded.

    Attributes:
        TRACK: Unpaved roads that only allow very slow driving speed or may require
               an off-road capable vehicle.
        RESTRICTED: Roads that are not publicly accessible and may require a special permit.
    """

    TRACK = "track"
    RESTRICTED = "restricted"


class Driving(BaseModel):
    type: Literal["driving"] = "driving"
    disable_border_crossing: Optional[bool] = None
    traffic_model: Optional[DrivingTrafficModel] = None
    include_roads: Optional[List[IncludeRoads]] = None


class Walking(BaseModel):
    type: Literal["walking"] = "walking"


class Cycling(BaseModel):
    type: Literal["cycling"] = "cycling"


class Ferry(BaseModel):
    type: Literal["ferry", "cycling+ferry", "driving+ferry"] = "ferry"
    boarding_time: Optional[int] = None
    traffic_model: Optional[DrivingTrafficModel] = None
    include_roads: Optional[List[IncludeRoads]] = None

    @model_validator(mode="after")
    def check_traffic_model(self):
        if self.type != "driving+ferry" and self.traffic_model:
            raise ValueError(
                '"traffic_model" cannot be specified when type is not "driving+ferry"'
            )
        return self

    @model_validator(mode="after")
    def check_include_roads(self):
        if self.type != "driving+ferry" and self.include_roads:
            raise ValueError(
                '"include_roads" cannot be specified when type is not "driving+ferry"'
            )
        return self


class DrivingTrain(BaseModel):
    type: Literal["driving+train"] = "driving+train"
    pt_change_delay: Optional[int] = None
    driving_time_to_station: Optional[int] = None
    parking_time: Optional[int] = None
    walking_time: Optional[int] = None
    boarding_time: Optional[int] = None
    max_changes: Optional[MaxChanges] = None
    traffic_model: Optional[DrivingTrafficModel] = None


class DrivingPublicTransport(BaseModel):
    type: Literal["driving+public_transport"] = "driving+public_transport"
    pt_change_delay: Optional[int] = None
    driving_time_to_station: Optional[int] = None
    parking_time: Optional[int] = None
    walking_time: Optional[int] = None
    boarding_time: Optional[int] = None
    max_changes: Optional[MaxChanges] = None
    traffic_model: Optional[DrivingTrafficModel] = None


class PublicTransport(BaseModel):
    type: Literal["public_transport", "train", "bus", "coach"] = "public_transport"
    pt_change_delay: Optional[int] = None
    walking_time: Optional[int] = None
    max_changes: Optional[MaxChanges] = None


class CyclingPublicTransport(BaseModel):
    type: Literal["cycling+public_transport"] = "cycling+public_transport"
    walking_time: Optional[int] = None
    pt_change_delay: Optional[int] = None
    cycling_time_to_station: Optional[int] = None
    parking_time: Optional[int] = None
    boarding_time: Optional[int] = None
    max_changes: Optional[MaxChanges] = None


class TransportationFastType(str, Enum):
    PUBLIC_TRANSPORT = "public_transport"
    DRIVING = "driving"
    CYCLING = "cycling"
    WALKING = "walking"
    WALKING_FERRY = "walking+ferry"
    CYCLING_FERRY = "cycling+ferry"
    DRIVING_FERRY = "driving+ferry"
    DRIVING_PUBLIC_TRANSPORT = "driving+public_transport"


class FastTrafficModel(str, Enum):
    """Only applicable with driving and driving+ferry transportation types.

    Attributes:
        PEAK: Represents typical traffic conditions for a midweek morning (default)
        OFF_PEAK: Represents typical traffic conditions at nighttime
    """

    PEAK = "peak"
    OFF_PEAK = "off_peak"


class PublicTransportFast(BaseModel):
    type: Literal["public_transport"] = "public_transport"
    walking_time: Optional[int] = None


class WalkingFast(BaseModel):
    type: Literal["walking"] = "walking"


class CyclingFast(BaseModel):
    type: Literal["cycling"] = "cycling"


class DrivingFast(BaseModel):
    type: Literal["driving"] = "driving"
    traffic_model: Optional[FastTrafficModel] = None


class WalkingFerryFast(BaseModel):
    type: Literal["walking+ferry"] = "walking+ferry"


class CyclingFerryFast(BaseModel):
    type: Literal["cycling+ferry"] = "cycling+ferry"


class DrivingFerryFast(BaseModel):
    type: Literal["driving+ferry"] = "driving+ferry"
    traffic_model: Optional[FastTrafficModel] = None


class DrivingPublicTransportFast(BaseModel):
    type: Literal["driving+public_transport"] = "driving+public_transport"
    walking_time: Optional[int] = None
    driving_time_to_station: Optional[int] = None
    parking_time: Optional[int] = None
