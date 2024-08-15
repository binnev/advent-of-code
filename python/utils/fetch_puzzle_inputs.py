import asyncio
from datetime import datetime
from pathlib import Path

import aiofiles
from aiofiles import os
from aiohttp import ClientSession

BASE_DIR = Path(__file__).parent.parent.parent
INPUTS_DIR = BASE_DIR / ".puzzle-inputs"
AOC_SESSION_COOKIE_FILE = BASE_DIR / ".aoc-session"
FIRST_YEAR = 2015


def main():
    assert AOC_SESSION_COOKIE_FILE.exists()
    with open(AOC_SESSION_COOKIE_FILE) as file:
        aoc_session_cookie = file.read().strip()

    asyncio.run(_get_all_inputs(aoc_session_cookie))


async def _get_puzzle_input(year: int, day: int, session: ClientSession):
    filename = INPUTS_DIR / f"{year}/day{day}.txt"
    if filename.exists():
        print(f"{year=} {day=} already exists; skipping")
        return

    url = f"https://adventofcode.com/{year}/day/{day}/input"
    response = await session.request(method="GET", url=url)
    text = await response.text()
    if not response.ok:
        print(f"{year=} {day=} is not available yet: {text}")
        return

    async with aiofiles.open(filename, mode="w") as file:
        await file.write(text)
    print(f"{year=} {day=} fetched; saved to {filename}")


async def _get_all_inputs(cookie: str):
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
    await asyncio.gather(
        *(os.makedirs(INPUTS_DIR / str(year), exist_ok=True) for year in years)
    )
    # fetch the inputs
    async with ClientSession(
        headers={"Cookie": f"session={cookie}"}
    ) as session:
        await asyncio.gather(
            *(
                _get_puzzle_input(year, day, session)
                for year, day_range in jobs
                for day in day_range
            )
        )


if __name__ == "__main__":
    main()
