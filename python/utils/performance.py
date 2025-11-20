import functools
import time
from typing import Callable, ParamSpec, TypeVar

T = TypeVar("T")
P = ParamSpec("P")


def profile(func: Callable[P, T]) -> Callable[P, T]:
    @functools.wraps(func)
    def wrapped(*args: P.args, **kwargs: P.kwargs):
        t1 = time.perf_counter()
        result = func(*args, **kwargs)
        t2 = time.perf_counter()
        print(f"{func.__name__}: {result} ({t2 - t1:.5f} seconds)")
        return result

    return wrapped
