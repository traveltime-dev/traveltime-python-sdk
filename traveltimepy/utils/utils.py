from traveltimepy.dto.requests.request import TravelTimeRequest
from traveltimepy.dto.requests.time_filter import TimeFilterRequest


def count_api_hits(request: TravelTimeRequest) -> int:
    if isinstance(request, TimeFilterRequest):
        return len(request.departure_searches) + len(request.arrival_searches)
    raise TypeError(f"Unsupported request type: {type(request)}")
