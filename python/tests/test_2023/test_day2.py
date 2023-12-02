import utils
from puzzles.y2023 import day2

example1 = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""


def test_parse_game():
    input = "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue"
    assert day2.parse_game(input) == (
        2,
        [
            day2.RgbTuple(blue=1, green=2, red=0),
            day2.RgbTuple(green=3, blue=4, red=1),
            day2.RgbTuple(green=1, blue=1, red=0),
        ],
    )


def test_part1():
    assert day2.part1(example1) == 8
    input = utils.load_puzzle_input("2023/day2")
    assert day2.part1(input) == 1853


def test_get_min_cubes():
    games = day2.parse_games(example1)
    results = []
    for ii, game in games:
        results.append(day2.get_min_cubes(game))
    assert results[0] == day2.RgbTuple(red=4, green=2, blue=6)
    assert results[1] == day2.RgbTuple(red=1, green=3, blue=4)


def test_part2():
    assert day2.part2(example1) == 2286
    input = utils.load_puzzle_input("2023/day2")
    assert day2.part2(input) == 72706
