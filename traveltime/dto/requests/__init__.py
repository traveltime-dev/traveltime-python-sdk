from pydantic import BaseModel


class Rectangle(BaseModel):
    min_lat: float
    max_lat: float
    min_lng: float
    max_lng: float
