from importlib import import_module
from pathlib import Path

import pytest

solutions_file = Path(__file__).parent.parent / "solutions.txt"
assert solutions_file.exists()
with open(solutions_file) as file:
    lines = file.read().strip().split("\n")

parameters = []
for string in lines:
    day, part, answer = string.split(", ")
    module = import_module(f"_2020.python.{day}")
    func = getattr(module, part)
    answer = int(answer)
    parameters.append((day, func, answer))


@pytest.mark.parametrize("day, func, expected_output", parameters)
def test(day, func, expected_output):
    assert func() == expected_output
