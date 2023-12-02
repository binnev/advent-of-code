import re
from dataclasses import dataclass

import utils


@dataclass
class RgbTuple:
    red: int = 0
    green: int = 0
    blue: int = 0


def parse_game(game: str) -> tuple[int, list[RgbTuple]]:
    rx = re.compile(r"Game (\d+): (.*)")
    match = rx.match(game)
    game, rest = match.groups()
    game = int(game)
    cube_groups = list(map(str.strip, rest.split(";")))
    cube_colours = []
    rx = re.compile(r"(\d+) (blue|red|green)")
    for group in cube_groups:
        matches = rx.findall(group)
        kwargs = {color: int(n) for n, color in matches}
        cube_colours.append(RgbTuple(**kwargs))
    return game, cube_colours


def parse_games(input: str) -> list[tuple[int, list[RgbTuple]]]:
    return [parse_game(line) for line in input.splitlines()]


def is_game_possible(game: list[RgbTuple], limit: RgbTuple) -> bool:
    for hand in game:
        if hand.red > limit.red or hand.blue > limit.blue or hand.green > limit.green:
            return False
    return True


@utils.profile
def part1(input: str):
    limit = RgbTuple(red=12, green=13, blue=14)
    result = 0
    games = parse_games(input)
    for ii, game in games:
        if is_game_possible(game, limit):
            result += ii
    return result


def get_min_cubes(game: list[RgbTuple]) -> RgbTuple:
    minimum = RgbTuple(red=0, green=0, blue=0)
    for hand in game:
        minimum.red = max(minimum.red, hand.red)
        minimum.blue = max(minimum.blue, hand.blue)
        minimum.green = max(minimum.green, hand.green)
    return minimum


@utils.profile
def part2(input: str):
    games = parse_games(input)
    result = 0
    for _, game in games:
        min_cubes = get_min_cubes(game)
        power = min_cubes.red * min_cubes.blue * min_cubes.green
        result += power
    return result


if __name__ == "__main__":
    input = utils.load_puzzle_input("2023/day2")
    assert part1(input) == 1853
    assert part2(input) == 72706
