from puzzles.y2023 import day3


example1 = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

example2 = """123...
....45"""


def test_part1():
    assert day3.part1(example1) == 4361


def test_part2():
    assert day3.part2(example1) == 467835


def test__find_all_number_coords():
    lines = day3._parse_input(example2)
    result = day3._find_all_number_coords(lines)
    assert result == {
        ((0, 0), (1, 0), (2, 0)): 123,
        ((4, 1), (5, 1)): 45,
    }
