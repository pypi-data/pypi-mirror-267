from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Tuple, Type


class ExceptionFunctionReturnType(Enum):
    """
    Controls how the given handler function should be treated after it
    is called. NoReturn types will be added to the exception message while
    Return types will be returned.
    """

    NoReturn = auto()
    Return = auto()


class ExceptionHandlerFunctionBase(ABC):
    """Base class for exception handling functions."""

    @abstractmethod
    def handle(
        self,
        function: Callable,
        function_args: Tuple[Any, ...],
        function_kwargs: Dict[str, Any],
        exception: Exception,
    ) -> Tuple[Any, ExceptionFunctionReturnType]:
        """
        Handles the exception and returns a value if needed. If a value is returned,
        then the FunctionReturnType is set to 'Return'.

        Parameters
        ----------
        function : Callable
            The managed/handled function.
        function_args : Tuple[Any, ...]
            The arguments of the function.
        function_kwargs : Dict[str, Any]
            The key-value arguments of the function.
        exception : Exception
            Exception that was raised.

        Returns
        -------
        Tuple[Any, FunctionReturnType]
            A tuple where the first object can be any object and the second is
            a return type.
        """
        pass


@dataclass
class ExceptionHandler:
    """Class for handling exceptions."""

    exception: Type[Exception]
    function: ExceptionHandlerFunctionBase


class GroupExceptionHandler:
    """
    Class for handling cases when multiple exceptions have the same handler
    function.
    """

    def __init__(
        self, exceptions: List[Type[Exception]], function: ExceptionHandlerFunctionBase
    ) -> None:
        self.handlers = [
            ExceptionHandler(exception, function) for exception in exceptions
        ]
