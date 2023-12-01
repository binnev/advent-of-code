from datetime import datetime

import requests
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
INPUTS_DIR = BASE_DIR / "_inputs"
AOC_SESSION_COOKIE_FILE = BASE_DIR / ".aoc-session"
FIRST_YEAR = 2015


def main():
    assert INPUTS_DIR.exists()
    assert AOC_SESSION_COOKIE_FILE.exists()
    with open(AOC_SESSION_COOKIE_FILE) as file:
        aoc_session_cookie = file.read()

    this_year = datetime.today().year
    _get_all_inputs(aoc_session_cookie, this_year)


def _require_file(path: Path):
    print(f"Checking {path} exists... ", end="")
    if not path.exists():
        raise FileNotFoundError(path.as_posix())
    print("OK")


def _get_puzzle_input(year: int, day: int, cookie: str):
    target_filename = INPUTS_DIR / f"{year}/day{day}.txt"
    if target_filename.exists():
        return

    url = f"https://adventofcode.com/{year}/day/{day}/input"
    response = requests.get(url=url, cookies={"session": cookie})

    if response.status_code > 200:
        print("Not available yet; stopping.")
        exit(1)
    else:
        with open(target_filename, "w") as file:
            file.write(response.text)


def _get_all_inputs(cookie: str, this_year: int):
    print("Fetching puzzle inputs...")
    for year in range(FIRST_YEAR, this_year + 1):
        print(f"{year}:", end=" ")
        (INPUTS_DIR / str(year)).mkdir(exist_ok=True)  # Make sure the folder exists.
        for day in range(1, 26):
            _get_puzzle_input(year, day, cookie)
            print(f"{day}", end=" ")
        print("")


if __name__ == "__main__":
    main()
