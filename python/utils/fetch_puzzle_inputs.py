from datetime import datetime

import requests
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
INPUTS_DIR = BASE_DIR / "_inputs"
assert INPUTS_DIR.exists()

AOC_SESSION_COOKIE_FILE = BASE_DIR / ".aoc-session"
assert AOC_SESSION_COOKIE_FILE.exists()
with open(AOC_SESSION_COOKIE_FILE) as file:
    AOC_SESSION_COOKIE = file.read()


FIRST_YEAR = 2015
THIS_YEAR = datetime.today().year


def main():
    _get_all_inputs()


def _require_file(path: Path):
    print(f"Checking {path} exists... ", end="")
    if not path.exists():
        raise FileNotFoundError(path.as_posix())
    print("OK")


def _get_puzzle_input(year: int, day: int):
    target_filename = INPUTS_DIR / f"{year}/day{day}.txt"
    if target_filename.exists():
        return

    url = f"https://adventofcode.com/{year}/day/{day}/input"
    response = requests.get(url=url, cookies={"session": AOC_SESSION_COOKIE})

    if response.status_code > 200:
        print("Not available yet; stopping.")
        exit(1)
    else:
        with open(target_filename, "w") as file:
            file.write(response.text)


def _get_all_inputs():
    print("Fetching puzzle inputs...")
    for year in range(FIRST_YEAR, THIS_YEAR + 1):
        print(f"{year}:", end=" ")
        (INPUTS_DIR / str(year)).mkdir(exist_ok=True)  # Make sure the folder exists.
        for day in range(1, 26):
            _get_puzzle_input(year, day)
            print(f"{day}", end=" ")
        print("")


if __name__ == "__main__":
    main()
