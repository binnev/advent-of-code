raw = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

raw = """7777838353
2217272478
3355318645
2242618113
7182468666
5441641111
4773862364
5717125521
7542127721
4576678341"""


class Octopus:
    def __init__(self, energy):
        self.energy = energy

    def __repr__(self):
        return f"{self.energy}"

    def __str__(self):
        return self.__repr__()


class Board:
    def __init__(self):
        self.contents = [list(map(Octopus, row)) for row in init()]
        self.flashes = 0

    def __repr__(self):
        return "\n".join("".join(map(str, row)) for row in self.contents)

    def update(self):
        flashed = set()
        for oct in self.octopi:
            oct.energy += 1

        while ready_to_flash := [
            (x, y, oct)
            for y, row in enumerate(self.contents)
            for x, oct in enumerate(row)
            if oct.energy > 9 and oct not in flashed
        ]:
            for x, y, oct in ready_to_flash:
                flashed.add(oct)
                for neighbour in self.get_neighbours(x, y):
                    neighbour.energy += 1

        for oct in flashed:
            oct.energy = 0
        return flashed

    def get_neighbours(self, x, y):
        directions = [
            (x - 1, y - 1),
            (x - 1, y),
            (x - 1, y + 1),
            (x, y - 1),
            (x, y + 1),
            (x + 1, y - 1),
            (x + 1, y),
            (x + 1, y + 1),
        ]
        octos = []
        for x, y in directions:
            if x < 0 or y < 0:
                continue
            try:
                octos.append(self.contents[y][x])
            except IndexError:
                pass
        return octos

    @property
    def octopi(self):
        return [o for row in self.contents for o in row]


def init():
    return [list(map(int, row)) for row in raw.splitlines()]


def get_neighbours(x, y):
    return [
        (x - 1, y - 1),
        (x - 1, y),
        (x - 1, y + 1),
        (x, y - 1),
        (x, y + 1),
        (x + 1, y - 1),
        (x + 1, y),
        (x + 1, y + 1),
    ]


def update1(octopi):
    flashed = set()
    # update energy level
    for y, row in enumerate(octopi):
        for x, oct in enumerate(row):
            octopi[y][x] += 1

    # do flashes
    while ready_to_flash := [
        (x, y)
        for y, row in enumerate(octopi)
        for x, oct in enumerate(row)
        if oct > 9 and (x, y) not in flashed
    ]:
        for (x, y) in ready_to_flash:
            flashed.add((x, y))
            for a, b in get_neighbours(x, y):
                if a < 0 or b < 0:
                    continue
                try:
                    octopi[b][a] += 1
                except IndexError:
                    pass
    for x, y in flashed:
        octopi[y][x] = 0  # reset to 0
    return flashed


def part1():
    board = Board()
    num_flashes = 0
    for ii in range(100):
        flashes = board.update()
        num_flashes += len(flashes)
    return num_flashes


def part2():
    octopi = init()
    ii = 0
    while True:
        ii += 1
        update1(octopi)
        energies = set(oct for row in octopi for oct in row)
        if energies == {0}:
            return ii


if __name__ == "__main__":
    print(f"part1: {part1()}")
    print(f"part2: {part2()}")
    assert part1() == 1721
    assert part2() == 298
