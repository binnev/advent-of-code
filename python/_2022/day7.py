from python import utils

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


class Folder(dict):
    parent: "Folder|None"

    def __init__(self, parent, *args, **kwargs):
        self.parent = parent

    def get_size(self) -> int:
        return sum(item.get_size() if isinstance(item, Folder) else item for item in self.values())


def explore_folders(input: str) -> Folder:
    root = cwd = Folder(parent=None)
    mode = ""
    for line in input.split("\n"):

        # handle commands
        if line.startswith("$"):
            _, cmd = line.split(" ", maxsplit=1)

            match cmd.split():
                case ["cd", dir_name]:
                    match dir_name:
                        case "..":
                            cwd = cwd.parent
                        case "/":
                            cwd = root
                        case _:
                            cwd = cwd[dir_name]
                case ["ls"]:
                    mode = "ls"

        else:  # not a command
            if mode == "ls":
                match line.split():
                    case ["dir", dir_name]:
                        cwd[dir_name] = Folder(parent=cwd)
                    case [file_size, file_name]:
                        cwd[file_name] = int(file_size)
    return root


def find_under_100000(folder: Folder):
    total_size = 0
    size = folder.get_size()
    if size <= 100000:
        total_size += size

    for name, value in folder.items():
        if isinstance(value, Folder):
            total_size += find_under_100000(value)

    return total_size


@utils.profile
def part1() -> int:
    input = utils.load_puzzle_input("2022/day7")
    root = explore_folders(input)
    return find_under_100000(root)


def all_folder_sizes(folder: Folder) -> list[int]:
    all_sizes = []
    all_sizes.append(folder.get_size())

    for name, value in folder.items():
        if isinstance(value, Folder):
            all_sizes.extend(all_folder_sizes(value))

    return all_sizes


@utils.profile
def part2() -> int:
    TOTAL_SPACE = 70_000_000
    REQUIRED_SPACE = 30_000_000
    input = utils.load_puzzle_input("2022/day7")
    root = explore_folders(input)
    occupied_space = root.get_size()
    unused_space = TOTAL_SPACE - occupied_space
    need_to_delete = REQUIRED_SPACE - unused_space
    all_sizes = all_folder_sizes(root)
    return min(s for s in all_sizes if s > need_to_delete)


if __name__ == "__main__":
    assert part1() == 1792222
    assert part2() == 1112963
