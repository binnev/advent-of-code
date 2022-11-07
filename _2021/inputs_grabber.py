from pathlib import Path
import requests

if __name__ == "__main__":
    for ii in range(1, 26):
        path = Path(__file__).parent / "puzzle_inputs" / f"day{ii}.txt"
        response = requests.get(f"https://adventofcode.com/2021/day/{ii}/input")
        print
