import re
from collections import namedtuple

import utils

Range = namedtuple("Range", "start, stop")
Transform = dict[Range, Range]


@utils.profile
def part1(input: str):
    seeds, transforms = _parse_input(input)

    lowest = seeds[0]
    for seed in seeds:
        seed = _calculate_seed(seed, transforms)
        if seed < lowest:
            lowest = seed
    return lowest


@utils.profile
def part2(input: str):
    seeds, transforms = _parse_input(input)
    seed_ranges = []
    for ii in range(0, len(seeds) // 2 + 1, 2):
        start = seeds[ii]
        width = seeds[ii + 1]
        seed_range = range(start, start + width)
        seed_ranges.append(seed_range)

    counter = 0
    total = sum((sr.stop - sr.start) for sr in seed_ranges)
    lowest = seed_ranges[0].start
    for seed_range in seed_ranges:
        for seed in seed_range:
            seed = _calculate_seed(seed, transforms)
            counter += 1
            print(f"{counter}/{total}")
            if seed < lowest:
                lowest = seed
    return lowest


def _find_critical_points(transforms: list[Transform]) -> set[int]:
    critical_points = set()
    # working backwards from the rightmost transform
    for trans in reversed(transforms):
        # for any existing critical points;
        # if they intersect this transform, then transform the
        # points "left". Otherwise just leave them as-is.
        new = set()
        for pt in critical_points:
            pt_transformed_left = _apply_map_backwards(pt, trans)
            new.add(pt_transformed_left)
        critical_points = new

        # all the edges of the input ranges are automatically critical points
        for input_range in trans:
            critical_points.add(input_range[0])
            critical_points.add(input_range[1])
    return critical_points


def _contains_value(r: Range, value: int) -> bool:
    return r[0] <= value <= r[1]


def _overlaps(first: Range, second: Range) -> bool:
    (s1, e1), (s2, e2) = first, second
    return (e1 >= s2 and e2 >= s1) or (e2 >= s1 and e1 >= s2)


def _contains(first: Range, second: Range) -> bool:
    (s1, e1), (s2, e2) = first, second
    return (s2 >= s1 and e2 <= e1) or (s1 >= s2 and e1 <= e2)


def _intersect(first: Range, second: Range) -> list[Range]:
    points = sorted([first[0], first[1], second[0], second[1]])
    out = [
        (points[0], points[1] - 1),
        (points[1], points[2]),
        (points[2] + 1, points[3]),
    ]
    return out


def _calculate_seed(seed: int, transforms: list[Transform]) -> int:
    for transform in transforms:
        seed = _apply_map(seed, transform)
    return seed


def _parse_range_line(line: str) -> tuple[Range, Range]:
    dst, src, width = list(map(int, line.split()))
    src_range = Range(start=src, stop=src + width - 1)
    dst_range = Range(start=dst, stop=dst + width - 1)
    return src_range, dst_range


def _apply_map(input: int, transform: Transform) -> int:
    for in_range, out_range in transform.items():
        if _contains_value(in_range, input):
            offset = input - in_range.start
            return out_range.start + offset
    # if no ranges match, output = input
    return input


def _apply_map_backwards(input: int, transform: Transform) -> int:
    for in_range, out_range in transform.items():
        if _contains_value(out_range, input):
            offset = input - out_range[0]
            return in_range[0] + offset
    return input


def _parse_input(input: str) -> tuple[list[int], list[Transform]]:
    lines = input.splitlines()
    seed_line = lines.pop(0)
    input = "\n".join(lines)
    seeds = list(map(int, re.findall(r"(\d+)", seed_line)))

    transform = None
    transforms = []
    for line in input.splitlines():
        if line.endswith("map:"):
            if transform:
                transforms.append(transform)
            transform = Transform()
        elif line.strip():
            src_range, dst_range = _parse_range_line(line)
            transform[src_range] = dst_range
    transforms.append(transform)

    return seeds, transforms


if __name__ == "__main__":
    input = utils.load_puzzle_input("2023/day5")
    # part2(input)
    print(input)
