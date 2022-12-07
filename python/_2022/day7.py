from pprint import pprint

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
        size = 0
        for name, value in self.items():
            if isinstance(value, Folder):
                size += value.get_size()
            else:
                size += value
        return size


def explore_folders(input: str) -> Folder:
    root = cwd = Folder(parent=None)
    mode = ""
    for line in input.split("\n"):

        # handle commands
        if line.startswith("$"):
            _, cmd = line.split(" ", maxsplit=1)

            if cmd.startswith("cd"):
                _, dir_name = cmd.split(" ", maxsplit=1)
                if dir_name == "..":
                    try:
                        cwd = cwd.parent
                    except AttributeError as e:
                        raise e
                elif dir_name == "/":
                    cwd = root
                else:
                    cwd = cwd[dir_name]

            elif cmd.startswith("ls"):
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


TOTAL_SPACE = 70_000_000
REQUIRED_SPACE = 30_000_000


def all_folder_sizes(folder: Folder) -> list[int]:
    all_sizes = []
    all_sizes.append(folder.get_size())

    for name, value in folder.items():
        if isinstance(value, Folder):
            all_sizes.extend(all_folder_sizes(value))

    return all_sizes


@utils.profile
def part2() -> int:
    input = utils.load_puzzle_input("2022/day7")
    root = explore_folders(input)
    occupied_space = root.get_size()
    unused_space = TOTAL_SPACE - occupied_space
    need_to_delete = REQUIRED_SPACE - unused_space
    all_sizes = all_folder_sizes(root)
    return min(s for s in all_sizes if s > need_to_delete)


if __name__ == "__main__":
    part1()
    part2()
