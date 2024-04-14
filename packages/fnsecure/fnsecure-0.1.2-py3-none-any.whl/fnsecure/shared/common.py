from dataclasses import dataclass
from typing import Dict, List, Type

from .exception_types import ExceptionHandler


@dataclass
class FunctionDescriptor:
    """
    Contains all relevant information about the function.

    Parameters
    ----------
    name : str
        The name of the function.
    exceptions : List[Type[Exception]]
        All the exceptions that the given function can raise.
    exception_handlers : List[ExceptionHandler]
        Contains all exception handlers for the given function at a given time.
    """

    name: str
    exceptions: List[Type[Exception]]
    exception_handlers: List[ExceptionHandler]


class Context:
    """
    Manages a given context and it contains all managed functions in this
    context.
    """

    def __init__(self) -> None:
        self._functions: Dict[str, FunctionDescriptor] = {}

    def register(self, func_desc: FunctionDescriptor) -> None:
        """Register a function if it is not registered already."""
        _func = self._functions.get(func_desc.name, None)
        if _func:
            return

        self._functions[func_desc.name] = func_desc

    def get_function_exceptions(self, func_name: str) -> List[Type[Exception]]:
        """Returns the registered list of exception for the given function."""
        return self._functions[func_name].exceptions

    def update_handler_list(
        self, function_name: str, handlers: List[ExceptionHandler]
    ) -> None:
        """
        Updates the handlers list given the managed function's name.

        Parameters
        ----------
        function_name : str
            The name of the managed/handled function.
        handlers : List[ExceptionHandler]
            The new list of ExceptionHandlers to use.
        """
        _func = self._functions.get(function_name, None)
        assert (
            _func
        ), f"Handlers cannot be updated because function {function_name} is not registered."

        self._functions[function_name].exception_handlers = handlers

    def get_handler_list(self, function_name: str) -> List[ExceptionHandler]:
        """
        Returns the list of handlers given the managed function's name.
        Returns an empty list in case the attribute was not set up.
        """
        _handlers = self._functions.get(function_name, None).exception_handlers
        return _handlers if _handlers else []


_MAIN_CONTEXT = Context()
