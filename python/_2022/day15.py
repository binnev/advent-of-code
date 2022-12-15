import math
import re
from math import sqrt

from python import utils
from python._2022.day14 import SparseMatrix, print_sparse_matrix, Coord

example = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""


SensorList = list[tuple[Coord, Coord, int]]  # sensor, beacon, distance


def parse_input(input: str) -> (SparseMatrix, SensorList):
    rx = re.compile("Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")
    sensor_list: SensorList = []
    grid = SparseMatrix()
    for line in input.splitlines():
        match = rx.search(line)
        sensor_x, sensor_y, beacon_x, beacon_y = map(int, match.groups())
        sensor = (sensor_x, sensor_y)
        beacon = (beacon_x, beacon_y)
        distance = manhattan_dist(sensor, beacon)
        sensor_list.append((sensor, beacon, distance))
        grid[sensor] = "S"
        grid[beacon] = "B"
    return grid, sensor_list


def manhattan_dist(a: Coord, b: Coord) -> int:
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return dx + dy


def sensor_contains(sensor: Coord, range: int, point: Coord) -> bool:
    dist = manhattan_dist(sensor, point)
    return dist <= range


def possible_xys(dist: int) -> list[Coord]:
    for x in range(int(dist) + 1):
        y = dist - x
        yield (x, y)


def exclude_sensor(sensor: Coord, beacon: Coord, grid: SparseMatrix):
    sensor_x, sensor_y = sensor
    dist_to_beacon = manhattan_dist(sensor, beacon)
    for dist in range(dist_to_beacon + 1):
        for x, y in possible_xys(dist):
            for flip_x in [-1, 1]:
                for flip_y in [-1, 1]:
                    pt = (
                        sensor_x + x * flip_x,
                        sensor_y + y * flip_y,
                    )
                    grid[pt] = grid.get(pt) or "#"


@utils.profile
def part1():
    """
    4814446 too low
    5631712 too low
    5696158 too low
    5716881 bingo!
    """
    # input, row_y = example, 10
    input, row_y = utils.load_puzzle_input("2022/day15"), 2000000
    grid, sensor_list = parse_input(input)

    # get the min/max x-bounds of all sensors; this is our x search space (points whose x-value
    # COULD intersect a sensor's range)
    min_x = math.inf
    max_x = -math.inf
    for sensor, beacon, dist in sensor_list:
        x, y = sensor
        sensor_min_x = x - dist
        sensor_max_x = x + dist
        if sensor_min_x < min_x:
            min_x = sensor_min_x
        if sensor_max_x > max_x:
            max_x = sensor_max_x

    # scan all possible x values and check if they intersect a sensor
    no_beacons = 0  # spaces where there can be no beacons
    search_space = max_x - min_x
    print(f"{search_space=}")
    for x in range(min_x, max_x + 1):
        if x % 100000 == 0:
            percent_done = (x - min_x) / search_space * 100
            print(f"{percent_done:.2f}% done; blocked {no_beacons} so far")

        point = (x, row_y)
        value = grid.get(point)
        if value == "B":
            continue  # a beacon is here, it can't be blocked for beacons
        if value == "S":
            no_beacons += 1  # a sensor is here; no beacons can be here
            continue

        for sensor, _, sensor_range in sensor_list:
            if sensor_contains(sensor, sensor_range, point):
                no_beacons += 1
                break
    return no_beacons


def tuning_freq(x: int, y: int) -> int:
    return x * 4000000 + y


@utils.profile
def part2():
    min_x = min_y = 0
    # input, max_x, max_y = example, 20, 20
    input, max_x, max_y = utils.load_puzzle_input("2022/day15"), 4000000,4000000
    grid, sensor_list = parse_input(input)

    search_space = (max_x-min_x) * (max_y-min_y)
    print(f"{search_space=}")
    ii = 0
    for x in range(min_x, max_x+1):
        for y in range(min_y, max_y+1):
            if not any(
                sensor_contains(sensor, sensor_range, (x, y))
                for sensor, _, sensor_range in sensor_list
            ):
                return tuning_freq(x, y)
            ii += 1
            if x % 1000000 == 0:
                percent_done = (ii) / search_space * 100
                print(f"{percent_done:.10f}% done")


if __name__ == "__main__":
    assert part1() == 5716881
    # part2()
