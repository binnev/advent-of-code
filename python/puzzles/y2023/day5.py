import re

import utils

RangeMap = dict[range, range]


@utils.profile
def part1(input: str):
    seeds, maps = _parse_input(input)

    lowest = seeds[0]
    for seed in seeds:
        seed = _calculate_seed(seed, maps)
        if seed < lowest:
            lowest = seed
    return lowest


@utils.profile
def part2(input: str):
    ...


def _calculate_seed(seed: int, maps: list[RangeMap]) -> int:
    for range_map in maps:
        seed = _apply_map(seed, range_map)
    return seed


def _parse_range_line(line: str) -> tuple[range, range]:
    dst, src, width = list(map(int, line.split()))
    src_range = range(src, src + width)
    dst_range = range(dst, dst + width)
    return src_range, dst_range


def _apply_map(input: int, mapp: RangeMap) -> int:
    for in_range, out_range in mapp.items():
        if input in in_range:
            offset = input - in_range.start
            return out_range.start + offset
    # if no ranges match, output = input
    return input


def _parse_input(input: str) -> tuple[list[int], list[RangeMap]]:
    lines = input.splitlines()
    seed_line = lines.pop(0)
    input = "\n".join(lines)
    seeds = list(map(int, re.findall(r"(\d+)", seed_line)))

    range_map = None
    maps = []
    for line in input.splitlines():
        if line.endswith("map:"):
            if range_map:
                maps.append(range_map)
            range_map = RangeMap()
        elif line.strip():
            src_range, dst_range = _parse_range_line(line)
            range_map[src_range] = dst_range
    maps.append(range_map)

    return seeds, maps


if __name__ == "__main__":
    input = utils.load_puzzle_input("2023/day5")
    part1(input)
