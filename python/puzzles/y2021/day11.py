import utils


class Octopus:
    def __init__(self, energy):
        self.energy = energy

    def __repr__(self):
        return f"{self.energy}"

    def __str__(self):
        return self.__repr__()


class Board:
    def __init__(self, raw: str):
        self.contents = [list(map(Octopus, row)) for row in init(raw)]

    def __repr__(self):
        return "\n".join("".join(map(str, row)) for row in self.contents)

    def update(self):
        flashes = set()
        for oct in self.octopi:
            oct.energy += 1

        while ready_to_flash := [
            (x, y, oct)
            for y, row in enumerate(self.contents)
            for x, oct in enumerate(row)
            if oct.energy > 9 and oct not in flashes
        ]:
            for x, y, oct in ready_to_flash:
                flashes.add(oct)
                for neighbour in self.get_neighbours(x, y):
                    neighbour.energy += 1

        for oct in flashes:
            oct.energy = 0
        return flashes

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


def init(raw: str):
    return [list(map(int, row)) for row in raw.splitlines()]


@utils.profile
def part1(raw: str):
    board = Board(raw)
    num_flashes = 0
    for ii in range(100):
        flashes = board.update()
        num_flashes += len(flashes)
    return num_flashes


@utils.profile
def part2(raw: str):
    board = Board(raw)
    ii = 0
    while True:
        ii += 1
        board.update()
        energies = set(oct.energy for row in board.contents for oct in row)
        if energies == {0}:
            return ii


if __name__ == "__main__":
    raw = utils.load_puzzle_input("2021/day11")
    assert part1(raw) == 1721
    assert part2(raw) == 298
