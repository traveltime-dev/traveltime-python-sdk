from typing import Literal

from pydantic.main import BaseModel


class Driving(BaseModel):
    type: Literal['driving'] = 'driving'


class Bus(BaseModel):
    type: Literal['bus'] = 'bus'


class PublicTransport(BaseModel):
    type: Literal['public_transport'] = 'public_transport'
