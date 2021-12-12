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

# raw = """start-A
# start-b
# A-c
# A-b
# b-d
# A-end
# b-end"""

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

        if neighbour.islower() and (neighbour in path) and small_cave_visited_twice(path):
            continue

        # recursive case
        foo = dfs2(path + [neighbour])
        new_paths.extend(foo)

    return new_paths


def part1():
    paths = dfs(["start"])
    return len(paths)


def small_cave_visited_twice(path):
    for node in {p for p in path if p.islower()}:
        if path.count(node) > 1:
            return True
    return False


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
