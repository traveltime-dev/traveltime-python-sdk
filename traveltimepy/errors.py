from typing import Dict, List


class TravelTimeError(Exception):
    pass


class TravelTimeServerError(TravelTimeError):
    def __init__(self, error: str):
        super(TravelTimeServerError, self).__init__(error)


class TravelTimeApiError(TravelTimeError):
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


class TravelTimeJsonError(TravelTimeApiError):
    status_code: int
    error_code: str
    description: str
    documentation_link: str
    additional_info: Dict[str, List[str]]

    def __init__(
        self,
        status_code: int,
        error_code: str,
        description: str,
        documentation_link: str,
        additional_info: Dict[str, List[str]],
    ):
        self.status_code = status_code
        self.error_code = error_code
        self.description = description
        self.documentation_link = documentation_link
        self.additional_info = additional_info

        super(TravelTimeJsonError, self).__init__(
            self.status_code,
            self.error_code,
            {
                **self.additional_info,
                self.description: [self.description],
                self.documentation_link: [self.documentation_link],
            },
        )


class TravelTimeProtoError(TravelTimeApiError):
    status_code: int
    error_code: str
    error_details: str
    error_message: str

    def __init__(
        self, status_code: int, error_code: str, error_details: str, error_message: str
    ):
        self.status_code = status_code
        self.error_code = error_code
        self.error_details = error_details
        self.error_message = error_message

        super(TravelTimeProtoError, self).__init__(
            self.status_code,
            self.error_code,
            {
                "X-ERROR-DETAILS": [self.error_details],
                "X-ERROR-MESSAGE": [self.error_message],
            },
        )
