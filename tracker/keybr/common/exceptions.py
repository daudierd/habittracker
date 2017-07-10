"""
Exceptions that may happen in all the keybr api code.
"""

class KeybrException(Exception):
    """Base exception."""

    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        exception_msg = "Message: %s\n" % self.msg
        return exception_msg

class TimeoutException(KeybrException):
    """Triggered when keybr website takes too long to reach the database"""

    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        exception_msg = "Message: %s\n" % self.msg
        return exception_msg
