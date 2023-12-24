import utils
from utils import SparseMatrix3, Coord3


@utils.profile
def part1(input: str) -> int:
    pass


@utils.profile
def part2(input: str) -> int:
    pass


def parse_input(source: str) -> SparseMatrix3:
    matrix = SparseMatrix3()
    xs = ys = zs = 0
    for ii, line in enumerate(source.splitlines()):
        left, right = line.split("~")
        x1, y1, z1 = map(int, left.split(","))
        x2, y2, z2 = map(int, right.split(","))
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        dz = abs(z1 - z2)
        if [dx, dy, dz].count(0) < 2:
            raise Exception(f"This one is not linear: {line}")

        if dx > 0:
            xs += 1
        elif dy > 0:
            ys += 1
        elif dz > 0:
            zs += 1
    print(f"{xs=}, {ys=}, {zs=}")


if __name__ == "__main__":
    source = utils.load_puzzle_input("2023/day22")
    parse_input(source)
