from typing import Sequence, TypeVar

# sparse matrix key types
Coord = tuple[int, int]
Coord3 = tuple[int, int, int]
T = TypeVar("T", str, int)  # sparse matrix value type

#test
class SparseMatrix(dict[Coord, T]):
    def get_xlim(self) -> tuple[int, int]:
        return get_sparse_matrix_xlim(self)

    def get_ylim(self) -> tuple[int, int]:
        return get_sparse_matrix_ylim(self)

    def print(self, flip_y=False, pad=0, empty_char="."):
        print_sparse_matrix(self, flip_y, pad, empty_char)

    def to_str(self, flip_y=False, pad=0, empty_char="."):
        return sparse_matrix_string(self, flip_y, pad, empty_char)

    @classmethod
    def from_str(cls, source: str, ignore: str = "") -> "SparseMatrix":
        return sparse_matrix_from_string(source, ignore)


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

    lines = list[str]()
    y_start = min_y - pad
    y_stop = max_y + 1 + pad
    x_start = min_x - pad
    x_stop = max_x + 1 + pad
    for y in range(y_start, y_stop):
        line = ""
        for x in range(x_start, x_stop):
            line += str(grid.get((x, y), empty_char))
        lines.append(line)
    if flip_y:
        lines = reversed(lines)
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


def sparse_matrix_from_string(source: str, ignore: str = "") -> SparseMatrix:
    matrix = SparseMatrix()
    for yy, line in enumerate(source.splitlines()):
        for xx, char in enumerate(line):
            coord = (xx, yy)
            if char in ignore:
                continue
            else:
                matrix[coord] = char
    return matrix
