"""
Exceptions that may happen in all the keybr api code.
"""

class HabiticaApiException(Exception):
    """Base exception."""

    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        exception_msg = "Message: %s\n" % self.msg
        return exception_msg

class LoginException(HabiticaApiException):
    """
    Thrown when the user couldn't log in the API.
    This may happen when the credentials provided by the user are incorrect.
    """

    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        exception_msg = "Message: %s\n" % self.msg
        return exception_msg

class ParameterException(HabiticaApiException):
    """
    Thrown when parameters provided by the user are not supported by the API.
    """

    def __init__(self, msg=None, expected_params=None):
        # expected_params should be a list of string values allowed by the api
        self.msg = msg
        self.expected_params = expected_params

    def __str__(self):
        exception_msg = "Message: %s\n" % self.msg \
                        + "Parameters values expected: " \
                        + str.join(', ', self.expected_params)
        return exception_msg
