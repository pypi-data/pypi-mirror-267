import functools
from collections.abc import Callable
from typing import TypeVar

T = TypeVar('T')


def wraps(wrapped: T) -> Callable[[Callable], T]:
    def wrapper(func: Callable) -> T:
        @functools.wraps(wrapped)
        def inner(*args, **kwargs):
            return func(*args, **kwargs)

        return inner

    return wrapper
