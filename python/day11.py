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
        self.has_flashed = False

    def __repr__(self):
        return f"{self.energy}"

    def __str__(self):
        return self.__repr__()

    @property
    def ready_to_flash(self):
        return self.energy > 9 and not self.has_flashed

    def flash(self):
        self.energy = 0
        self.has_flashed = True


class Board:
    def __init__(self, raw):
        self.raw = raw
        self.contents = init()
        self.flashes = 0

    def __repr__(self):
        return "\n".join("".join(map(str, row)) for row in self.contents)

    def update(self):
        # update all octopuses' energy level
        for oct in self.octopi:
            oct.energy += 1
            oct.has_flashed = False

        while self.ready_to_flash:
            self.do_flashes()

    def do_flashes(self):
        for y, row in enumerate(self.contents):
            for x, oct in enumerate(row):
                if oct.ready_to_flash:
                    oct.flash()
                    self.flashes += 1
                    for neighbour in self.get_neighbours(x, y):
                        neighbour.energy += 1

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

    @property
    def ready_to_flash(self):
        return any(oct.ready_to_flash for oct in self.octopi)


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
            # flash
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
    octopi = init()
    num_flashes = 0
    print("before any flashes")
    print("\n".join("".join(map(str, row)) for row in octopi))

    for ii in range(100):
        flashes = update1(octopi)
        num_flashes += len(flashes)
        print("")
        print(f"iteration {ii+1}")
        print("\n".join("".join(map(str, row)) for row in octopi))
    return num_flashes


def part2():
    pass


if __name__ == "__main__":
    print(f"part1: {part1()}")
    print(f"part2: {part2()}")
