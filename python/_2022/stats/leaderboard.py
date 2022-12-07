import datetime
import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.axes import Axes


def load_file() -> dict:
    json_file = Path(__file__).parent / "leaderboard.json"
    with open(json_file) as file:
        data = json.load(file)

    for member_data in data["members"].values():
        if member_data["name"] is None:
            member_data["name"] = f"Anonymous user {member_data['id']}"

    return data


def day_part_score(data: dict, day: int, part: int) -> dict[str:int]:
    """
    [Local Score], which awards users on this leaderboard points much like the global
    leaderboard. If you add or remove users, the points will be recalculated, and the order can
    change.

    For N users, the first user to get each star gets N points, the second gets N-1, and the last
    gets 1. This is the default.
    """
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
    days = [datetime.datetime(2022, 12, x, 6, 0, 0) for x in range(1, 26)]
    timestamps = [d.timestamp() for d in days]
    ax.set_xticks(timestamps)
    ax.set_xticklabels(x.day for x in days)
    ax.set_xlabel("Day")
    ax.grid(which="major", axis="x")

    scores = calc_scores(data)
    members = []
    for member_data in data["members"].values():
        name = member_data["name"]
        member = {}
        timestamps, member_score = get_score_member(scores, name=name)
        score = member_score[-1]
        member["score"] = score
        handles = ax.step(
            timestamps,
            member_score,
            label=name,
            where="post",
            lw=3,
        )
        member["handle"] = handles[0]
        member["label"] = f"{name} ({score})"
        members.append(member)
        try:
            timestamp = next(ts for ts in reversed(timestamps) if ts is not None)
            ax.plot(timestamp, score, ".k")
            ax.text(x=timestamp, y=score, s=str(score))
        except StopIteration:
            pass  # no points at all yet so don't print score

    leaderboard = sorted(members, key=lambda m: -m["score"])
    handles = [member["handle"] for member in leaderboard]
    labels = [member["label"] for member in leaderboard]
    ax.legend(
        handles,
        labels,
        loc="best",  # "lower right",
        fontsize="x-small",
    )
    plt.show()


if __name__ == "__main__":
    data = load_file()
    plot_results(data)
