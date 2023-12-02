from typing import NamedTuple

import utils
import re


class RgbTuple(NamedTuple):
    red: int
    green: int
    blue: int


def parse_game(game: str):
    rx = re.compile(r"Game (\d+): (.*)")
    match = rx.match(game)
    game, rest = match.groups()
    game = int(game)
    cube_groups = list(map(str.strip, rest.split(";")))
    cube_colours = []
    rx = re.compile(r"(\d+) (blue|red|green)")
    for group in cube_groups:
        red = green = blue = 0
        matches = rx.findall(group)
        for match in matches:
            n, colour = match
            if colour == "green":
                green = int(n)
            if colour == "blue":
                blue = int(n)
            if colour == "red":
                red = int(n)
        cube_colours.append(RgbTuple(red=red, green=green, blue=blue))
    return game, cube_colours


def is_game_possible(game: list[RgbTuple], max_red: int, max_blue: int, max_green: int) -> bool:
    for hand in game:
        if hand.red > max_red or hand.blue > max_blue or hand.green > max_green:
            return False
    return True


@utils.profile
def part1(input: str):
    max_red = 12
    max_green = 13
    max_blue = 14
    result = 0
    games = [parse_game(line) for line in input.splitlines()]
    for ii, game in games:
        if is_game_possible(game, max_red=max_red, max_blue=max_blue, max_green=max_green):
            result += ii

    return result


@utils.profile
def part2(input: str):
    return ""


if __name__ == "__main__":
    input = utils.load_puzzle_input("2023/day2")
    assert part1(input) == 1853
