import asyncio
from datetime import datetime
from pathlib import Path

from aiofiles import os
import aiofiles
import requests
from aiohttp import ClientSession

BASE_DIR = Path(__file__).parent.parent.parent
INPUTS_DIR = BASE_DIR / "_inputs"
AOC_SESSION_COOKIE_FILE = BASE_DIR / ".aoc-session"
FIRST_YEAR = 2015


def main():
    assert AOC_SESSION_COOKIE_FILE.exists()
    with open(AOC_SESSION_COOKIE_FILE) as file:
        aoc_session_cookie = file.read()

    asyncio.run(_bulk_get_puzzle_inputs_async(aoc_session_cookie))


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


async def _get_puzzle_input_async(year: int, day: int, session: ClientSession):
    filename = INPUTS_DIR / f"{year}/day{day}.txt"
    if filename.exists():
        print(f"{year=} {day=} already exists; skipping")
        return

    url = f"https://adventofcode.com/{year}/day/{day}/input"
    response = await session.request(method="GET", url=url)
    if not response.ok:
        print(f"{year=} {day=} is not available yet")
        return

    text = await response.text()

    async with aiofiles.open(filename, mode="w") as file:
        await file.write(text)
    print(f"{year=} {day=} fetched; saved to {filename}")


async def _bulk_get_puzzle_inputs_async(cookie: str):
    today = datetime.today()
    this_year = today.year
    this_month = today.month
    this_day = today.day
    is_december = this_month == 12

    # only consider the current year if it is december
    years = range(FIRST_YEAR, this_year + 1 if is_december else this_year)
    jobs = []
    for year in years:
        # for the current year, only get up to today's puzzle. For previous years, get them all
        max_day = this_day + 1 if year == this_year else 26
        jobs.append((year, range(1, max_day)))

    # make sure all the year dirs exist first
    await asyncio.gather(*(os.makedirs(INPUTS_DIR / str(year), exist_ok=True) for year in years))
    # fetch the inputs
    async with ClientSession(cookies={"session": cookie}) as session:
        await asyncio.gather(
            *(
                _get_puzzle_input_async(year, day, session)
                for year, day_range in jobs
                for day in day_range
            )
        )


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
