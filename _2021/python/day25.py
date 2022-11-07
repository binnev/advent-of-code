from copy import copy
from _2021.python import utils

raw = utils.load_puzzle_input("day25")


class CucumberField(dict):
    def calculate_size(self):
        self.width, self.height = size(self)


def init(raw_string):
    cucumbers = CucumberField()
    for y, line in enumerate(raw_string.splitlines()):
        for x, char in enumerate(line):
            cucumbers[(x, y)] = char
    cucumbers.calculate_size()
    return cucumbers


def print_stuff(things):
    xs = [x for x, y in things]
    ys = [y for x, y in things]
    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            print(things[(x, y)], end="")
        print("")


def size(cucumbers):
    xs = [x for x, y in cucumbers]
    ys = [y for x, y in cucumbers]
    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)
    return (max_x - min_x) + 1, (max_y - min_y) + 1


def can_move(coords, cucumbers):
    x, y = coords
    cucumber = cucumbers[coords]
    if cucumber == ">":
        next_coords = ((x + 1) % cucumbers.width), y
    if cucumber == "v":
        next_coords = x, ((y + 1) % cucumbers.height)
    return next_coords if cucumbers[next_coords] == "." else False


def move(coords, new_coords, cucumbers):
    if new_coords:
        cucumbers[new_coords] = cucumbers.pop(coords)
        cucumbers[coords] = "."


def iterate(cucumbers):
    east_movers = [
        (coords, new_coords)
        for coords, cucumber in cucumbers.items()
        if cucumber == ">" and (new_coords := can_move(coords, cucumbers))
    ]
    for coords, new_coords in east_movers:
        move(coords, new_coords, cucumbers)

    south_movers = [
        (coords, new_coords)
        for coords, cucumber in cucumbers.items()
        if cucumber == "v" and (new_coords := can_move(coords, cucumbers))
    ]
    for coords, new_coords in south_movers:
        move(coords, new_coords, cucumbers)


@utils.profile
def part1():
    cucumbers = init(raw)
    ii = 1
    while True:
        copycumbers = copy(cucumbers)
        iterate(cucumbers)
        if cucumbers == copycumbers:
            break
        ii += 1
    return ii


if __name__ == "__main__":
    assert part1() == 295
