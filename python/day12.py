raw = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

# raw= """dc-end
# HN-start
# start-kj
# dc-start
# dc-HN
# LN-dc
# HN-end
# kj-sa
# kj-HN
# kj-dc
# """
#
# raw = """YW-end
# DK-la
# la-XG
# end-gy
# zq-ci
# XG-gz
# TF-la
# xm-la
# gy-gz
# ci-start
# YW-ci
# TF-zq
# ci-DK
# la-TS
# zq-YW
# gz-YW
# zq-gz
# end-gz
# ci-TF
# DK-zq
# gy-YW
# start-DK
# gz-DK
# zq-la
# start-TF"""

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

def dfs2(path):
    node = path[-1]
    new_paths = []
    for neighbour in links[node]:
        if neighbour.islower() and path.count(neighbour) >= 2:
            continue

        # base case -- finish
        if neighbour == "end":
            new_paths.append(path + [neighbour])
            continue

        # recursive case
        foo = dfs2(path + [neighbour])
        new_paths.extend(foo)

    return new_paths


def part1():
    paths = dfs(["start"])
    # for path in paths:
    #     print(",".join(path))
    return len(paths)


def part2():
    paths = dfs2(["start"])
    for path in paths:
        print(",".join(path))
    return len(paths)


if __name__ == "__main__":
    print(f"part1: {part1()}")
    print(f"part2: {part2()}")
