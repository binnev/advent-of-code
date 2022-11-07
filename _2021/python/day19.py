import re
from collections import deque
from itertools import combinations
from pprint import pprint

from _2021.python import utils

raw = utils.load_puzzle_input("day19")


def print_stuff(things):
    xs = [x for x, y in things]
    ys = [-y for x, y in things]
    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            print(things.get((x, -y), "."), end="")
        print("")


def init():
    input = raw.split("\n\n")
    scanners = dict()
    for text in input:
        lines = text.splitlines()
        scanner = int(re.findall("\d+", lines.pop(0))[0])
        scanners[scanner] = d = dict()
        # d[(0, 0, 0)] = "S"
        for line in lines:
            x, y, z = list(map(int, line.split(",")))
            d[(x, y, z)] = "B"

    return scanners


def match_scanners(scanner0, scanner1):
    # loop: try matching every beacon on scanner1 to every beacon in scanner0
    for (x0, y0, z0) in scanner0:
        for (x1, y1, z1) in scanner1:
            # will need to shift the x,y of all scanner2 to achieve this.
            dx = x0 - x1
            dy = y0 - y1
            dz = z0 - z1
            shifted1 = {(x + dx, y + dy, z + dz): value for (x, y, z), value in scanner1.items()}

            # if, after the shift, 3 beacons overlap, it's a match
            hits = set(shifted1).intersection(scanner0)
            if len(hits) > 11:
                return (dx, dy, dz), shifted1
    return False, None


def match_axis(scanner0, scanner1):
    xs0 = [x for (x, y, z) in scanner0]
    xs1 = [x for (x, y, z) in scanner1]
    for p1, x0 in enumerate(xs0):
        for p2, x1 in enumerate(xs1):
            # will need to shift the x,y of all scanner2 to achieve this.
            dx = x0 - x1
            shifted1 = [(x + dx) for x in xs1]

            # if, after the shift, 3 beacons overlap, it's a match
            hits = set(shifted1).intersection(xs0)
            if len(hits) > 11:
                return dx, p1, p2
    return None, None, None


def rotate_scanner(scanner, x=0, y=1, z=2, flip_x=False, flip_y=False, flip_z=False):
    rotated = {
        (
            coords[x] * (-1 if flip_x else 1),
            coords[y] * (-1 if flip_y else 1),
            coords[z] * (-1 if flip_z else 1),
        ): value
        for coords, value in scanner.items()
    }
    return rotated


def get_orientations():
    orientations = []
    xs = (0, 1, 2)
    for x in xs:
        ys = set(xs).difference({x})
        for y in ys:
            for z in set(ys).difference({y}):
                for flip_x in (True, False):
                    for flip_y in (True, False):
                        for flip_z in (True, False):
                            orientations.append((x, y, z, flip_x, flip_y, flip_z))
    return orientations


def find_matching_points(scanner0, scanner1):
    xs = (0, 1, 2)
    for x_axis in xs:
        for flip_x in (True, False):
            rotated1 = rotate_scanner(scanner1, x=x_axis, flip_x=flip_x)
            # todo: not match_axis; that is trying all the points again.
            #  We just need to check if the orientation matches for the *given* points
            dx, p1, p2 = match_axis(scanner0, rotated1)
            if dx:
                return x_axis, flip_x, dx, p1, p2


def smart_stuff(scanner0, scanner1):
    x_axis, flip_x, dx, p1, p2 = find_matching_points(scanner0, scanner1)
    ys = {0, 1, 2}.difference({x_axis})
    for y in ys:
        z = set(ys).difference({y}).pop()
        for flip_y in (True, False):
            for flip_z in (True, False):
                rotated1 = rotate_scanner(scanner1, x, y, z, flip_x, flip_y, flip_z)
                dxdydz, shifted1 = match_scanners(scanner0, rotated1)
                if dxdydz:
                    return dxdydz, shifted1

    return False, False


@utils.profile
def part1():
    scanners = init()
    master = {**scanners.pop(0)}
    scanners = deque([(key, value) for key, value in scanners.items()])
    while scanners:
        key, scanner = scanners.popleft()
        print(f"comparing scanner {key}")
        dxdydz, shifted = smart_stuff(master, scanner)
        if dxdydz:
            print(f"dxdydz={','.join(map(str, dxdydz))}")
            master.update(shifted)
        else:
            print(f"no match for scanner {key} yet")
            scanners.append((key, scanner))

    return len(master)


def manhattan_distance(xyz1, xyz2):
    x1, y1, z1 = xyz1
    x2, y2, z2 = xyz2
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)


@utils.profile
def part2():
    input = raw.splitlines()
    scanner_positions = {0: (0, 0, 0)}
    for ii, row in enumerate(input):
        if "dxdydz" in row:
            previous = input[ii - 1]
            scanner_number = re.findall("\d+", previous)[-1]
            dxdydz = row.split("=")[-1]
            dxdydz = tuple(map(int, dxdydz.split(",")))
            scanner_positions[int(scanner_number)] = dxdydz
    pprint(scanner_positions)

    max_distance = 0
    for key1, key2 in combinations(scanner_positions, r=2):
        pos1 = scanner_positions[key1]
        pos2 = scanner_positions[key2]
        distance = manhattan_distance(pos1, pos2)
        max_distance = max(max_distance, distance)
    return max_distance


if __name__ == "__main__":
    assert part1() == 428
    assert part2() == 12140
    # scanners = init()
    # result = smart_stuff(scanners[0], scanners[1])
    # print(result)
