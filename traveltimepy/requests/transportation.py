from enum import Enum
from typing import Optional
from typing_extensions import Literal

from pydantic.main import BaseModel
from pydantic import model_validator

from traveltimepy.requests.common import DrivingTrafficModel


class MaxChanges(BaseModel):
    enabled: bool
    limit: int


class Driving(BaseModel):
    type: Literal["driving"] = "driving"
    disable_border_crossing: Optional[bool] = None
    traffic_model: Optional[DrivingTrafficModel] = None


class Walking(BaseModel):
    type: Literal["walking"] = "walking"


class Cycling(BaseModel):
    type: Literal["cycling"] = "cycling"


class Ferry(BaseModel):
    type: Literal["ferry", "cycling+ferry", "driving+ferry"] = "ferry"
    boarding_time: Optional[int] = None
    traffic_model: Optional[DrivingTrafficModel] = None

    @model_validator(mode="after")
    def check_traffic_model(self):
        if self.type != "driving+ferry" and self.traffic_model:
            raise ValueError(
                '"traffic_model" cannot be specified when type is not "driving+ferry"'
            )
        return self


class DrivingTrain(BaseModel):
    type: Literal["driving+train"] = "driving+train"
    pt_change_delay: Optional[int] = None
    driving_time_to_station: Optional[int] = None
    parking_time: Optional[int] = None
    walking_time: Optional[int] = None
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


class TransportationFast(str, Enum):
    PUBLIC_TRANSPORT = "public_transport"
    DRIVING = "driving"
    CYCLING = "cycling"
    WALKING = "walking"
    WALKING_FERRY = "walking+ferry"
    CYCLING_FERRY = "cycling+ferry"
    DRIVING_FERRY = "driving+ferry"
    DRIVING_PUBLIC_TRANSPORT = "driving+public_transport"
