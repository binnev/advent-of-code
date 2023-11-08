import utils

example = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""


def explore_folders(raw: str) -> dict[str:int]:
    root = cwd = ""
    contents = {"/": 0}
    for line in raw.split("\n"):
        if line.startswith("$"):
            _, cmd = line.split(" ", maxsplit=1)
            match cmd.split():
                case ["cd", dir_name]:
                    match dir_name:
                        case "..":
                            cwd, _ = cwd.rsplit("/", maxsplit=1)
                        case "/":
                            cwd = root
                        case _:
                            cwd = "/".join([cwd, dir_name])

        else:  # must be lines following "ls"
            match line.split():
                case ["dir", dir_name]:
                    contents["/".join([cwd, dir_name])] = 0
                case [file_size, file_name]:
                    contents["/".join([cwd, file_name])] = int(file_size)
    return contents


def get_folder_size(contents: dict[str:int], folder_path: str) -> int:
    return sum(
        size
        for path, size in contents.items()
        if path.startswith(folder_path) and not path.endswith(folder_path)
    )


@utils.profile
def part1(raw: str) -> int:
    contents = explore_folders(raw)
    folders = {k for k, v in contents.items() if v == 0}
    total = 0
    for folder in folders:
        if (size := get_folder_size(contents, folder)) < 100000:
            total += size
    return total


@utils.profile
def part2(raw: str) -> int:
    contents = explore_folders(raw)
    TOTAL_SPACE = 70_000_000
    REQUIRED_SPACE = 30_000_000
    occupied_space = get_folder_size(contents, folder_path="/")
    unused_space = TOTAL_SPACE - occupied_space
    need_to_delete = REQUIRED_SPACE - unused_space

    folders = {k for k, v in contents.items() if v == 0}
    all_sizes = [get_folder_size(contents, f) for f in folders]
    return min(s for s in all_sizes if s > need_to_delete)


if __name__ == "__main__":
    raw = utils.load_puzzle_input("2022/day7")
    assert part1(raw) == 1792222
    assert part2(raw) == 1112963
