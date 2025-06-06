from enum import Enum


class TransportationFast(str, Enum):
    PUBLIC_TRANSPORT = "public_transport"
    DRIVING = "driving"
    CYCLING = "cycling"
    WALKING = "walking"
    WALKING_FERRY = "walking+ferry"
    CYCLING_FERRY = "cycling+ferry"
    DRIVING_FERRY = "driving+ferry"
    DRIVING_PUBLIC_TRANSPORT = "driving+public_transport"