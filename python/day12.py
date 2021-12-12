raw = """YW-end
DK-la
la-XG
end-gy
zq-ci
XG-gz
TF-la
xm-la
gy-gz
ci-start
YW-ci
TF-zq
ci-DK
la-TS
zq-YW
gz-YW
zq-gz
end-gz
ci-TF
DK-zq
gy-YW
start-DK
gz-DK
zq-la
start-TF"""


links = dict()
for node1, node2 in [row.split("-") for row in raw.splitlines()]:
    links.setdefault(node1, []).append(node2)
    links.setdefault(node2, []).append(node1)


def dfs(path):
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
        foo = dfs(path + [neighbour])
        new_paths.extend(foo)

    return new_paths


def dfs2(path):
    node = path[-1]
    new_paths = []
    for neighbour in links[node]:
        if neighbour == "start":
            continue
        # base case -- finish
        if neighbour == "end":
            new_paths.append(path + [neighbour])
            continue

        # if neighbour.islower() and path.count(neighbour) >= 2:
        if neighbour.islower() and not check_small_cave_visits(path + [neighbour]):
            continue

        # recursive case
        foo = dfs2(path + [neighbour])
        new_paths.extend(foo)

    return new_paths


def part1():
    paths = dfs(["start"])
    return len(paths)


def check_small_cave_visits(path):
    counts = {node: path.count(node) for node in set(path) if node.islower()}
    if max(counts.values()) > 2:
        return False
    gt1 = list(filter(lambda k: counts[k] > 1, counts))
    return len(gt1) < 2


def part2():
    paths = dfs2(["start"])
    return len(paths)


if __name__ == "__main__":
    p1 = part1()
    print(f"part1: {p1}")
    p2 = part2()
    print(f"part2: {p2}")
    assert p1 == 4912
    assert p2 == 150004
