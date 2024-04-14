"""Contains all custom exceptions for this package."""


class UnHandledExceptionError(Exception):
    """Signals that an unexpected exception was raised."""

    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class HandledExceptionError(Exception):
    """Signals that an unexpected exception was raised."""

    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class FailedToContinueWithValue(Exception):
    """
    Signals that an error happened when tried to continue the function
    with a different value.
    """

    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class RetryFunctionCallFailed(Exception):
    """Signals that retying the function failed."""

    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class EmptyHandlerList(Exception):
    """
    Signals that the managed function has no handlers but an exception was
    raised.
    """

    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class HandlerSetupError(Exception):
    """Signals that the given handler cannot be set up for a given context."""

    def __init__(self, msg: str) -> None:
        super().__init__(msg)
