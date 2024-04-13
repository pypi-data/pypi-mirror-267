from typing import Any, Callable, List, Optional, Type

from ..errors import (
    EmptyHandlerList,
    HandledExceptionError,
    HandlerSetupError,
    UnHandledExceptionError,
)
from ..shared import _MAIN_CONTEXT, Context, FunctionDescriptor
from ..shared.exception_types import (
    ExceptionFunctionReturnType,
    ExceptionHandler,
    GroupExceptionHandler,
)
from .functions import RaiseWithMessage


def raises(
    function: str, exceptions: List[Type[Exception]], context: Optional[Context] = None
) -> Callable:
    """
    Registers the function. Handles exceptions when this function is called.

    Parameters
    ----------
    function : str
        The name of the function that should be registered.
    exceptions : List[Type[Exception]]
        The list of the exceptions the can occur.
    context : Optional[Context] = None
        The context object to use to store the function. Two decorators can only
        access the same function if they use the same context.

    Raises
    ------
    EmptyHandlerList
        When an exception was raised but there are no handlers set for the function.
    HandledExceptionError
        When an exception  and it was handled.
    UnHandledExceptionError
        When an exception was raised but it could not be handled with the given
        handlers.
    """
    _function = function
    _context = context if context else _MAIN_CONTEXT

    def register_function(function: str) -> None:
        """Register the function in the context."""

        _context.register(
            FunctionDescriptor(
                name=function, exceptions=exceptions, exception_handlers=[]
            )
        )

    register_function(function=_function)

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                _handlers = _context.get_handler_list(_function)
                if not _handlers:
                    error_msg = (
                        "Exception cannot be handled because no handlers "
                        + "were provided."
                    )
                    raise EmptyHandlerList(error_msg) from e

                for _handler in _handlers:
                    if type(e) == _handler.exception:
                        value, return_type = _handler.function.handle(
                            function=func,
                            function_args=args,
                            function_kwargs=kwargs,
                            exception=e,
                        )

                        if return_type == ExceptionFunctionReturnType.Return:
                            return value
                        else:
                            raise HandledExceptionError(value) from e

                error_msg = (
                    f"Function {func.__name__} has raised an unexpected "
                    + f"exception: {type(e)}. "
                    + "Consider adding this exception to the function. "
                )
                raise UnHandledExceptionError(error_msg) from e

        return wrapper

    return decorator


def handle(
    function: str,
    handlers: List[ExceptionHandler | GroupExceptionHandler],
    context: Optional[Context] = None,
) -> Callable:
    """
    Handles exceptions for the given function.

    Parameters
    ----------
    function: str
        The name of the managed function the should have its handlers updated.
    handlers : List[ExceptionHandler | GroupExceptionHandler]
        The function handlers will be updated with these ones.
    context : Optional[Context] = None
        The context in which the function is registered. By default every function
        is registered to the main context.
    Raises
    ------
    HandlerSetupError
        When the registered exceptions and the handled exception list are not
        matching.
    HandlerSetupError
        When there are unhandled exception.
    """
    _context = context if context else _MAIN_CONTEXT

    def normalize_exception_handlers(
        handlers: List[ExceptionHandler | GroupExceptionHandler],
    ) -> List[ExceptionHandler]:
        """All exception handlers should be of type ExceptionHandler."""
        _handlers = []
        for handler in handlers:
            if isinstance(handler, ExceptionHandler):
                _handlers.append(handler)
            elif isinstance(handler, GroupExceptionHandler):
                _handlers.extend([_handler for _handler in handler.handlers])

        return _handlers

    def verify_all_exceptions_handled(
        function: str, handlers: List[ExceptionHandler]
    ) -> None:
        """Raise an error if not all exceptions have been explicitly handled."""

        registered_exceptions = set(_context.get_function_exceptions(function))
        handled_exceptions = [handler.exception for handler in handlers]
        if len(handled_exceptions) != len(registered_exceptions):
            error_msg = (
                "Mismatch between registered and handled exceptions "
                + f"{handled_exceptions=} and {registered_exceptions=}."
            )
            raise HandlerSetupError(error_msg)

        handled_exceptions = set(handled_exceptions)
        unhandled_exceptions_count = len(registered_exceptions - handled_exceptions)
        if unhandled_exceptions_count != 0:
            error_msg = (
                f"Not all exceptions are handled for function {function}. "
                + "The following exceptions have been registered: "
                + f"{registered_exceptions} but only the following ones are "
                + f"handled: {handled_exceptions}"
            )

            raise HandlerSetupError(error_msg)

    handlers = normalize_exception_handlers(handlers)
    verify_all_exceptions_handled(function, handlers)

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            _context.update_handler_list(function_name=function, handlers=handlers)
            _result = func(*args, **kwargs)
            _context.update_handler_list(function_name=function, handlers=[])

            return _result

        return wrapper

    return decorator


def unhandled(function: str, context: Optional[Context] = None) -> Callable:
    """
    Marks the function as unhandled, meaning in the given context error
    handling is not needed. Same as calling
    `handle(function, [Handle(Exception, Raise()), ...])`
    """
    _context = context if context else _MAIN_CONTEXT

    message = (
        f"Function {function} was marked unhandled but it has thrown an exception."
    )
    all_handles = [
        GroupExceptionHandler(
            exceptions=_context.get_function_exceptions(function),
            function=RaiseWithMessage(message),
        )
    ]

    return handle(function=function, handlers=all_handles, context=_context)
