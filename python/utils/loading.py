from pathlib import Path


def load_puzzle_input(filename: str) -> str:
    path = Path(__file__).parent.parent.parent / f"_inputs/{filename}.txt"
    with open(path) as file:
        return file.read()


def load_solutions(year: str) -> list[list[str]]:
    path = Path(__file__).parent.parent.parent / f"_solutions/{year}.txt"
    with open(path) as file:
        contents = file.read()
    lines = contents.split("\n")
    return [line.split(", ") for line in lines]
