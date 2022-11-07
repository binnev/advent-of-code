from importlib import import_module
from pathlib import Path

import pytest

solutions_file = Path(__file__).parent.parent / "solutions.txt"
assert solutions_file.exists()
with open(solutions_file) as file:
    lines = file.read().strip().split("\n")

parameters = []
for day, string in enumerate(lines, start=1):
    part1_answer, part2_answer = string.split(", ")
    module = import_module(f"_2020.python.day{day}")
    part1_func = getattr(module, "part1")
    part2_func = getattr(module, "part2")
    part1_answer = int(part1_answer)
    part2_answer = int(part2_answer)
    parameters.append((f"day{day}", part1_func, part1_answer))
    parameters.append((f"day{day}", part2_func, part2_answer))


@pytest.mark.parametrize("day, func, expected_output", parameters)
def test(day, func, expected_output):
    assert func() == expected_output
