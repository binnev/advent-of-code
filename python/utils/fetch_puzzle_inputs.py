import asyncio
from asyncio import BoundedSemaphore
from datetime import date
from pathlib import Path
from typing import Awaitable

import aiofiles
from httpx import AsyncClient

BASE_DIR = Path(__file__).parent.parent.parent
INPUTS_DIR = BASE_DIR / ".puzzle-inputs"
AOC_SESSION_COOKIE_FILE = BASE_DIR / ".aoc-session"
FIRST_YEAR = 2015
MAX_CONCURRENT_REQUESTS = 3

Year = int
Day = int
Job = tuple[Year, Day]


async def main() -> None:
    """Fetch all the puzzle inputs."""
    assert AOC_SESSION_COOKIE_FILE.exists()
    with open(AOC_SESSION_COOKIE_FILE) as file:
        aoc_session_cookie = file.read().strip()

    client = AsyncClient(headers={"Cookie": f"session={aoc_session_cookie}"})
    sem = BoundedSemaphore(MAX_CONCURRENT_REQUESTS)
    jobs = _generate_years_and_days()
    coros = [_get_puzzle_input(year, day, client) for year, day in jobs]
    await asyncio.gather(*(rate_limited(coro, sem) for coro in coros))


async def rate_limited[T](coro: Awaitable[T], sem: BoundedSemaphore) -> T:
    async with sem:
        return await coro


async def _get_puzzle_input(year: int, day: int, client: AsyncClient) -> None:
    """Fetch 1 puzzle input and save it to file."""

    prefix = f"{year=} {day=}"
    filename = INPUTS_DIR / f"{year}/day{day}.txt"
    if filename.exists():
        print(f"{prefix} exists; skipping")
        return

    url = f"https://adventofcode.com/{year}/day/{day}/input"
    print(f"{year=} {day=} fetching...")
    response = await client.get(url)
    text = response.text
    if response.is_error:
        print(f"{year=} {day=} {response.status_code} ERROR: {text}")
        return

    # Only create the file if the request was successful
    filename.parent.mkdir(exist_ok=True, parents=True)
    async with aiofiles.open(filename, "w") as file:
        await file.write(text)
    print(f"{year=} {day=} fetched; saved to {filename}")


def _generate_years_and_days() -> list[tuple[Year, Day]]:
    today = date.today()
    this_year = today.year
    this_month = today.month
    this_day = today.day
    is_december = this_month == 12

    # only consider the current year if it is December. Otherwise we'll get lots
    # of unnecessary failures for unreleased puzzles.
    years = range(FIRST_YEAR, this_year + 1 if is_december else this_year)
    jobs: list[tuple[Year, Day]] = []
    for year in years:
        # for the current year, only get up to today's puzzle.
        # For previous years, get them all
        max_day = this_day + 1 if year == this_year else 26
        for day in range(1, max_day):
            jobs.append((year, day))

    # Reverse the jobs so we download the most recent day first
    return list(reversed(jobs))


if __name__ == "__main__":
    asyncio.run(main())
