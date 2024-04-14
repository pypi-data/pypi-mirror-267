"""Contains logic for exception handling functions."""

from typing import Any, Callable, Dict, Tuple

from ..errors import RetryFunctionCallFailed
from ..shared.exception_types import (
    ExceptionFunctionReturnType,
    ExceptionHandlerFunctionBase,
)


class Raise(ExceptionHandlerFunctionBase):
    """It raises the exception and does nothing else."""

    def handle(
        self,
        function: Callable,
        function_args: Tuple[Any, ...],
        function_kwargs: Dict[str, Any],
        exception: Exception,
    ) -> Tuple[Any, ExceptionFunctionReturnType]:
        return "", ExceptionFunctionReturnType.NoReturn


class RaiseWithMessage(ExceptionHandlerFunctionBase):
    """It raises the exception with the given message."""

    def __init__(self, message: str) -> None:
        self.message = message

    def handle(
        self,
        function: Callable,
        function_args: Tuple[Any, ...],
        function_kwargs: Dict[str, Any],
        exception: Exception,
    ) -> Tuple[Any, ExceptionFunctionReturnType]:
        return self.message, ExceptionFunctionReturnType.NoReturn


class Continue(ExceptionHandlerFunctionBase):
    """
    If an exception happens return with the specified value. The exception
    will not be thrown.
    """

    def __init__(self, return_value: Any) -> None:
        self.return_value = return_value

    def handle(
        self,
        function: Callable,
        function_args: Tuple[Any, ...],
        function_kwargs: Dict[str, Any],
        exception: Exception,
    ) -> Tuple[Any, ExceptionFunctionReturnType]:
        fixed_return_func = lambda *args, **kwargs: self.return_value

        return (
            fixed_return_func(*function_args, **function_kwargs),
            ExceptionFunctionReturnType.Return,
        )


class Retry(ExceptionHandlerFunctionBase):
    """
    Retries the function with the same parameters up to n times. It returns the
    value of the first successful function call.

    Raises
    -------
    RetryFunctionCallFailed
        If no function call was successful.
    """

    def __init__(self, n: int) -> Any:
        self.n = n

    def handle(
        self,
        function: Callable,
        function_args: Tuple[Any, ...],
        function_kwargs: Dict[str, Any],
        exception: Exception,
    ) -> Tuple[Any, ExceptionFunctionReturnType]:

        errors = []
        for _ in range(self.n):
            try:
                return (
                    function(*function_args, **function_kwargs),
                    ExceptionFunctionReturnType.Return,
                )
            except Exception as e:
                errors.append(e)

        error_msg = (
            f"Function {function.__name__} raised error {exception}."
            + f"This triggered {self.n} execution(s), "
            + "however all of them failed. "
            + f"The following exceptions were raised: {errors}\n"
        )
        raise RetryFunctionCallFailed(error_msg)


class RetryWithFunction(ExceptionHandlerFunctionBase):
    """When an exception happens runs the provided function instead."""

    def __init__(
        self, function: Callable, args: Tuple[Any], kwargs: Dict[str, Any]
    ) -> None:
        """
        Retry the execution with the provided parameters and arguments.

        Parameters
        ----------
        function : Callable
            The function to use in case of an exception.
        args : Tuple[Any]
            The arguments of the function.
        kwargs : Dict[str, Any]
            The keyword arguments of the function.

        Raises
        -------
        RetryFunctionCallFailed
            If the provided function throws an error.
        """

        self._func = function
        self._args = args
        self._kwargs = kwargs

    def handle(
        self,
        function: Callable,
        function_args: Tuple[Any, ...],
        function_kwargs: Dict[str, Any],
        exception: Exception,
    ) -> Tuple[Any, ExceptionFunctionReturnType]:

        try:
            return (
                self._func(*self._args, **self._kwargs),
                ExceptionFunctionReturnType.Return,
            )
        except Exception as e:
            error_msg = (
                f"The following exception: {exception} triggered an execution "
                + f"of function {self._func.__name__}. However, this execution "
                + f"has failed as well."
            )
            raise RetryFunctionCallFailed(error_msg) from e
