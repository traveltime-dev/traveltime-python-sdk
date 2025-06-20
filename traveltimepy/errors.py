from typing import Dict, List


class TravelTimeClientError(Exception):
    pass


class TravelTimeApiError(TravelTimeClientError):
    status_code: int
    error_code: str
    additional_info: Dict[str, List[str]]

    def __init__(
        self, status_code: int, error_code: str, additional_info: Dict[str, List[str]]
    ):
        self.status_code = status_code
        self.error_code = error_code
        self.additional_info = additional_info

        super(TravelTimeApiError, self).__init__(
            f"Travel Time API request failed with status code: {self.status_code}\n"
            f"Error code: {self.error_code}\n"
            f"Additional info: {self.additional_info}\n"
        )
