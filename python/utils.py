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


def prime_factors(number) -> dict[int:int]:
    """function to find the prime factors of a number by (modified) trial division.

    By default, the factors will be returned in dict format: {factor: exponent}:
    In [1]: prime_factors(24)
    Out[1]: {2: 3, 3: 1}
    Representing 24 = 2^3 * 3^1 = 2*2*2*3

    If optional argument output='list' is passed, the factors will be returned in list
    form:
    In [1]: prime_factors(24, output="list")
    Out[1]: [2, 2, 2, 3]
    """

    from math import sqrt

    factors = dict()
    if number == 0:
        return factors
    remainder = number
    product = 1
    p = 2
    limit = sqrt(number)

    # when the product of the factors equals the number itself, we know we've found
    # all the factors.
    while product != number:
        if p <= limit:
            while remainder % p == 0:
                factors[p] = factors.get(p, 0) + 1
                remainder = remainder // p
                product *= p
            p += 1 if p % 2 == 0 else 2  # skip even numbers
        else:
            if remainder != 1:
                factors[remainder] = factors.get(remainder, 0) + 1
                product *= remainder
    return factors
