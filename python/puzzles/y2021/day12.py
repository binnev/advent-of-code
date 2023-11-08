import utils


def init(raw: str):
    links = dict()
    for node1, node2 in [row.split("-") for row in raw.splitlines()]:
        links.setdefault(node1, []).append(node2)
        links.setdefault(node2, []).append(node1)
    return links


def dfs(path, links):
    node = path[-1]
    new_paths = []
    for neighbour in links[node]:
        if neighbour in path and neighbour.islower():
            continue

        # base case -- finish
        if neighbour == "end":
            new_paths.append(path + [neighbour])
            continue

        # recursive case
        foo = dfs(path + [neighbour], links)
        new_paths.extend(foo)

    return new_paths


def dfs2(path, links):
    node = path[-1]
    new_paths = []
    for neighbour in links[node]:
        if neighbour == "start":
            continue
        # base case -- finish
        if neighbour == "end":
            new_paths.append(path + [neighbour])
            continue

        if neighbour.islower() and (neighbour in path) and small_cave_visited_twice(path):
            continue

        # recursive case
        foo = dfs2(path + [neighbour], links)
        new_paths.extend(foo)

    return new_paths


@utils.profile
def part1(raw: str):
    links = init(raw)
    paths = dfs(["start"], links)
    return len(paths)


def small_cave_visited_twice(path):
    for node in {p for p in path if p.islower()}:
        if path.count(node) > 1:
            return True
    return False


@utils.profile
def part2(raw: str):
    links = init(raw)
    paths = dfs2(["start"], links)
    return len(paths)


if __name__ == "__main__":
    raw = utils.load_puzzle_input("2021/day12")
    assert part1(raw) == 4912
    assert part2(raw) == 150004
