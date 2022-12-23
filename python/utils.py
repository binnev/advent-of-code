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


Coord = tuple[int, int]
Coord3 = tuple[int, int, int]


class SparseMatrix(dict[Coord, str]):
    def print(self, flip_y=False, pad=0, empty_char="."):
        if self:
            xs = [x for x, y in self]
            ys = [(-y if flip_y else y) for x, y in self]
            min_x = min(xs)
            max_x = max(xs)
            min_y = min(ys)
            max_y = max(ys)
        else:
            min_x = max_x = min_y = max_y = 0
        for y in range(min_y - pad, max_y + 1 + pad):
            for x in range(min_x - pad, max_x + 1 + pad):
                print(self.get((x, (-y if flip_y else y)), empty_char), end="")
            print("")
        print("")


class SparseMatrix3(dict[Coord3, str]):
    def print(self, flip_y=False, pad=0, empty_char="."):
        min_z = min(z for x, y, z in self)
        max_z = max(z for x, y, z in self)
        for layer_z in range(min_z, max_z + 1):
            layer = SparseMatrix(
                {(x, y): value for (x, y, z), value in self.items() if z == layer_z}
            )
            layer.print(flip_y=flip_y, pad=pad, empty_char=empty_char)
