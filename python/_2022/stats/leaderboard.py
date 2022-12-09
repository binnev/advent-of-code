import datetime
import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from numpy import cumsum


def load_file() -> dict:
    json_file = Path(__file__).parent / "leaderboard.json"
    with open(json_file) as file:
        data = json.load(file)

    output = dict()
    for id, member in data["members"].items():
        if member["name"] is None:
            member["name"] = f"Anonymous user {member['id']}"

        # flatten and reformat completion details
        member["completion"] = {
            (int(dd), int(pp)): part
            for dd, day in member.pop("completion_day_level").items()
            for pp, part in day.items()
        }
        output[id] = member
    return output


def day_part_score(data: dict, day: int, part: int) -> dict[str:int]:
    """
    [Local Score], which awards users on this leaderboard points much like the global
    leaderboard. If you add or remove users, the points will be recalculated, and the order can
    change.

    For N users, the first user to get each star gets N points, the second gets N-1, and the last
    gets 1. This is the default.
    """
    solution_times = dict()
    scores = dict()
    for id, member in data.items():
        time = member["completion"].get((day, part), {}).get("get_star_ts")
        key = id
        if time is None:
            scores[key] = {"score": 0, "timestamp": None}
        else:
            solution_times[key] = time

    stars = len(data)
    for member, time in sorted(solution_times.items(), key=lambda kv: kv[1]):
        scores[member] = {"score": stars, "timestamp": time}
        stars -= 1
    return scores


def calc_scores(data: dict) -> dict:
    # we have to loop over the days and the parts, because for each day/part, we need to check
    # who has finished it and who hasn't.
    for day in range(1, 26):
        for part in range(1, 3):
            # label = f"{day}.{part}"
            scores = day_part_score(data, day=day, part=part)
            for id, score_data in scores.items():
                member = data[id]
                if daypart := member["completion"].get((day, part)):
                    daypart["score"] = score_data["score"]
    return data


def plot_results(data: dict):
    fig, ax = plt.subplots()
    ax: Axes
    ax.ticklabel_format(useOffset=False, style="plain")
    days = [datetime.datetime(2022, 12, x, 6, 0, 0) for x in range(1, 26)]
    timestamps = [d.timestamp() for d in days]
    ax.set_xticks(timestamps)
    ax.set_xticklabels(x.day for x in days)
    ax.set_xlabel("Day")
    ax.set_ylabel("Score")
    ax.grid(which="major", axis="x")

    leaderboard = sorted(data.values(), key=lambda x: -x["local_score"])
    for member in leaderboard:
        name = member["name"]
        stars = sorted(member["completion"].values(), key=lambda x: x["get_star_ts"])
        timestamps = [s["get_star_ts"] for s in stars]
        scores = list(cumsum([s["score"] for s in stars]))
        final_score = member["local_score"]
        handle, *_ = ax.step(
            timestamps,
            scores,
            label=f"{name} ({final_score})",
            where="post",
            lw=3,
        )
        if any(timestamps):
            last = timestamps[-1]
            ax.plot(last, final_score, ".k")
            ax.text(x=last, y=final_score, s=str(final_score))
    ax.legend(loc="best", fontsize="x-small")
    ax.set_title("* Christmas music intensifies *", weight="bold", fontsize="xx-large")
    plt.show()


if __name__ == "__main__":
    data = load_file()
    calc_scores(data)
    plot_results(data)
