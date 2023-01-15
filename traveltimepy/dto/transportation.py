from typing import Optional
from typing_extensions import Literal


from pydantic.main import BaseModel


class MaxChanges(BaseModel):
    enabled: bool
    limit: int


class Driving(BaseModel):
    type: Literal['driving'] = 'driving'
    disable_border_crossing: Optional[bool] = None


class Walking(BaseModel):
    type: Literal['walking'] = 'walking'


class Cycling(BaseModel):
    type: Literal['cycling'] = 'cycling'


class Ferry(BaseModel):
    type: Literal['ferry', 'cycling+ferry', 'driving+ferry'] = 'ferry'
    boarding_time: Optional[int] = None


class DrivingTrain(BaseModel):
    type: Literal['driving+train'] = 'driving+train'
    pt_change_delay: Optional[int] = None
    driving_time_to_station: Optional[int] = None
    parking_time: Optional[int] = None
    walking_time: Optional[int] = None
    max_changes: Optional[MaxChanges] = None


class PublicTransport(BaseModel):
    type: Literal[
        'public_transport',
        'train',
        'bus',
        'coach'
    ] = 'public_transport'
    pt_change_delay: Optional[int] = None
    walking_time: Optional[int] = None
    max_changes: Optional[int] = None
