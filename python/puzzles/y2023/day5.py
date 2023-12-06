import re

import utils

Transform = dict[range, range]


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


def _calculate_seed(seed: int, transforms: list[Transform]) -> int:
    for transform in transforms:
        seed = _apply_map(seed, transform)
    return seed


def _parse_range_line(line: str) -> tuple[range, range]:
    dst, src, width = list(map(int, line.split()))
    src_range = range(src, src + width)
    dst_range = range(dst, dst + width)
    return src_range, dst_range


def _apply_map(input: int, transform: Transform) -> int:
    for in_range, out_range in transform.items():
        if input in in_range:
            offset = input - in_range.start
            return out_range.start + offset
    # if no ranges match, output = input
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
    part2(input)
