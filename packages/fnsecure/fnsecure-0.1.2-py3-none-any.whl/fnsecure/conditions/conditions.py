"""Logic for precondition handling for functions."""

from typing import Callable, TypeVar

T = TypeVar("T")  # Represents the modified return type
R = TypeVar("R")  # Represents the original return type


def expects(
    precondition: Callable[..., bool], return_value: T
) -> Callable[[Callable[..., R]], Callable[..., T | R]]:
    """
    Enforces a precondition for a function; if the precondition is not met, the function
    returns with the specified value.

    Parameters
    ----------
    precondition : Callable[..., bool]
        A function that receives the same parameters as the target function and returns
        True if the precondition is satisfied, and False otherwise.
    return_value : T
        The value to return if the precondition is not satisfied.

    Returns
    -------
    Union[T, ReturnType]
        The return value of the target function if the precondition is satisfied, or
        the defined return value if the precondition is not satisfied.
    """

    def decorator(func: Callable[..., R]) -> Callable[..., T | R]:
        def wrapper(*args, **kwargs) -> T | R:
            if not precondition(*args, **kwargs):
                return return_value
            return func(*args, **kwargs)

        return wrapper

    return decorator
