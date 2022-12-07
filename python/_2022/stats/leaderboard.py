import datetime

import matplotlib.pyplot as plt
import json
from pathlib import Path
from pprint import pprint

from matplotlib.axes import Axes


def load_file() -> dict:
    json_file = Path(__file__).parent / "leaderboard.json"
    with open(json_file) as file:
        data = json.load(file)

    for member_id, member_data in data["members"].items():
        member_data["name"] = member_data["name"] or f"Anonymous user {member_data['id']}"

    return data


def day_part_score(data: dict, day: int, part: int) -> dict[str:int]:
    day = str(day)
    part = str(part)
    solution_times = dict()
    scores = dict()
    for member_id, member_data in data["members"].items():
        time = member_data["completion_day_level"].get(day, {}).get(part, {}).get("get_star_ts")
        key = member_data["name"]
        if time is None:
            scores[key] = {"score": 0, "timestamp": None}
        else:
            solution_times[key] = time

    stars = len(data["members"])
    for member, time in sorted(solution_times.items(), key=lambda kv: kv[1]):
        scores[member] = {"score": stars, "timestamp": time}
        stars -= 1
    return scores


def calc_scores(data: dict) -> dict[str:int]:
    scores = dict()
    for day in range(1, 26):
        for part in range(1, 3):
            scores[f"{day}.{part}"] = day_part_score(data, day=day, part=part)
    return scores


def get_score_member(scores: dict, name: str) -> tuple[list[int], list[int]]:
    xs, ys = [], []
    total_score = 0
    for day in range(1, 26):
        for part in range(1, 3):
            s = scores[f"{day}.{part}"][name]
            total_score += s["score"]
            xs.append(s["timestamp"])
            ys.append(total_score)
    return xs, ys


def plot_results(data: dict):
    fig, ax = plt.subplots()
    ax: Axes
    ax.ticklabel_format(useOffset=False, style="plain")
    days = [datetime.datetime(2022, 12, x, 6, 0, 0) for x in range(1, 16)]
    ax.set_xticks(days)
    ax.set_xticklabels(x.day for x in days)
    ax.set_xlabel("Day")
    ax.grid(which="major", axis="x")

    scores = calc_scores(data)
    members = [member["name"] for member in data["members"].values()]
    member_scores = dict()
    handles = []
    for member in members:
        timestamps, member_score = get_score_member(scores, name=member)
        member_scores[member] = member_score[-1]
        handle = ax.step(
            timestamps,
            member_score,
            label=member,
            where="post",
        )
        handles.append(handle)
        try:
            x, y = next(
                (ts, score)
                for ts, score in reversed(list(zip(timestamps, member_score)))
                if ts is not None
            )
            ax.plot(x, y, ".k")
            ax.text(x=x, y=y, s=str(y))
        except StopIteration:
            pass  # no points at all yet so don't print score

    # labels, handles = zip(
    #     (m, h) for (m, s), h in sorted(member_scores.items(), handles, key=lambda s_h: -s_h[0])
    # )
    ax.legend(loc="lower right", fontsize="x-small")
    plt.show()


if __name__ == "__main__":
    data = load_file()
    plot_results(data)
