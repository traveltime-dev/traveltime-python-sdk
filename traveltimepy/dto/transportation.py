from typing import Optional
from typing_extensions import Literal


from pydantic.main import BaseModel


class MaxChanges(BaseModel):
    enabled: bool
    limit: int

    def __hash__(self):
        return hash((self.enabled, self.limit))


class Driving(BaseModel):
    type: Literal["driving"] = "driving"
    disable_border_crossing: Optional[bool] = None

    def __hash__(self):
        return hash((self.type, self.disable_border_crossing))


class Walking(BaseModel):
    type: Literal["walking"] = "walking"

    def __hash__(self):
        return hash(self.type)


class Cycling(BaseModel):
    type: Literal["cycling"] = "cycling"

    def __hash__(self):
        return hash(self.type)


class Ferry(BaseModel):
    type: Literal["ferry", "cycling+ferry", "driving+ferry"] = "ferry"
    boarding_time: Optional[int] = None

    def __hash__(self):
        return hash((self.type, self.boarding_time))


class DrivingTrain(BaseModel):
    type: Literal["driving+train"] = "driving+train"
    pt_change_delay: Optional[int] = None
    driving_time_to_station: Optional[int] = None
    parking_time: Optional[int] = None
    walking_time: Optional[int] = None
    max_changes: Optional[MaxChanges] = None

    def __hash__(self):
        return hash(
            (
                self.type,
                self.pt_change_delay,
                self.driving_time_to_station,
                self.parking_time,
                self.walking_time,
                self.max_changes,
            )
        )


class PublicTransport(BaseModel):
    type: Literal["public_transport", "train", "bus", "coach"] = "public_transport"
    pt_change_delay: Optional[int] = None
    walking_time: Optional[int] = None
    max_changes: Optional[int] = None

    def __hash__(self):
        return hash((self.type, self.pt_change_delay, self.walking_time, self.max_changes))
