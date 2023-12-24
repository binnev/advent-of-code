from utils.fetch_puzzle_inputs import INPUTS_DIR


def load_puzzle_input(filename: str) -> str:
    path = INPUTS_DIR / f"{filename}.txt"
    with open(path) as file:
        return file.read()
