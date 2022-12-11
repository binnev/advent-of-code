import functools
import time
from pathlib import Path


def load_puzzle_input(filename: str) -> str:
    path = Path(__file__).parent.parent / f"puzzle_inputs/{filename}.txt"
    with open(path) as file:
        return file.read()


def load_solutions(year: str) -> list[list[str]]:
    path = Path(__file__).parent.parent / f"solutions/{year}.txt"
    with open(path) as file:
        contents = file.read()
    lines = contents.split("\n")
    return [line.split(", ") for line in lines]


def profile(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        t1 = time.perf_counter()
        result = func(*args, **kwargs)
        t2 = time.perf_counter()
        print(f"{func.__name__}: {result} ({t2-t1:.5f} seconds)")
        return result

    return wrapped
