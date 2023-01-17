import functools
import math
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


class SparseMatrix(dict[Coord, str | int]):
    def get_xlim(self) -> tuple[int, int]:
        return get_sparse_matrix_xlim(self)

    def get_ylim(self) -> tuple[int, int]:
        return get_sparse_matrix_ylim(self)

    def print(self, flip_y=False, pad=0, empty_char="."):
        print_sparse_matrix(self, flip_y, pad, empty_char)

    def to_str(self, flip_y=False, pad=0, empty_char="."):
        return sparse_matrix_string(self, flip_y, pad, empty_char)


class SparseMatrix3(dict[Coord3, str]):
    def get_xlim(self) -> tuple[int, int]:
        return get_sparse_matrix_xlim(self)

    def get_ylim(self) -> tuple[int, int]:
        return get_sparse_matrix_ylim(self)

    def get_zlim(self) -> tuple[int, int]:
        return get_sparse_matrix_zlim(self)

    def print(self, flip_y=False, pad=0, empty_char="."):
        print_sparse_matrix3(self, flip_y=flip_y, pad=pad, empty_char=empty_char)

    def plot(self):
        import numpy as np
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D

        min_x, max_x = self.get_xlim()
        min_y, max_y = self.get_ylim()
        min_z, max_z = self.get_zlim()
        x_width = max_x - min_x + 1
        y_width = max_y - min_y + 1
        z_width = max_z - min_z + 1
        filled = np.zeros((x_width, y_width, z_width), dtype=bool)
        for x, y, z in self:
            filled[x][y][z] = True

        ax: Axes3D = plt.figure().add_subplot(projection="3d")
        ax.voxels(
            filled,
            facecolors=[1, 0, 0, 1],
        )
        ax.set_aspect("equal")
        plt.show()


def get_sparse_matrix_xlim(grid: SparseMatrix | SparseMatrix3) -> tuple[int, int]:
    return min(pt[0] for pt in grid), max(pt[0] for pt in grid)


def get_sparse_matrix_ylim(grid: SparseMatrix | SparseMatrix3) -> tuple[int, int]:
    return min(pt[1] for pt in grid), max(pt[1] for pt in grid)


def get_sparse_matrix_zlim(grid: SparseMatrix | SparseMatrix3) -> tuple[int, int]:
    return min(pt[2] for pt in grid), max(pt[2] for pt in grid)


def sparse_matrix_string(grid: SparseMatrix, flip_y=False, pad=0, empty_char="."):
    min_x = max_x = min_y = max_y = 0
    if grid:
        min_x, max_x = get_sparse_matrix_xlim(grid)
        min_y, max_y = get_sparse_matrix_ylim(grid)
    if flip_y:
        min_y, max_y = -max_y, -min_y

    lines = list[str]()
    y_start = min_y - pad
    y_stop = max_y + 1 + pad
    x_start = min_x - pad
    x_stop = max_x + 1 + pad
    for y in range(y_start, y_stop):
        line = ""
        for x in range(x_start, x_stop):
            line += grid.get((x, (-y if flip_y else y)), empty_char)
        lines.append(line)
    return "\n".join(lines)


def print_sparse_matrix(grid: SparseMatrix, flip_y=False, pad=0, empty_char="."):
    print(sparse_matrix_string(grid, flip_y, pad, empty_char))


def print_sparse_matrix3(grid: SparseMatrix3, flip_y=False, pad=0, empty_char="."):
    if grid:
        min_z, max_z = get_sparse_matrix_zlim(grid)
    else:
        min_z = max_z = 0
    for layer_z in range(min_z, max_z + 1):
        layer = SparseMatrix({(x, y): value for (x, y, z), value in grid.items() if z == layer_z})
        print_sparse_matrix(layer, flip_y=flip_y, pad=pad, empty_char=empty_char)


if __name__ == "__main__":
    grid = SparseMatrix()
    grid[(0, 0)] = "A"
    grid[(2, 3)] = "B"
    grid.print()
