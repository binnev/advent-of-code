from math import inf

import utils


def init(raw: str):
    algorithm, raw_image = raw.split("\n\n")
    image = dict()
    for y, row in enumerate(raw_image.splitlines()):
        for x, pixel in enumerate(row):
            image[(x, y)] = 1 if pixel == "#" else 0
    return algorithm, image


def get_image_size(image):
    xs = [x for x, y in image]
    ys = [y for x, y in image]
    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)
    return (min_x, max_x), (min_y, max_y)


def print_image(image):
    (min_x, max_x), (min_y, max_y) = get_image_size(image)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            pixel = image.get((x, y))
            pixel = "#" if pixel else "."
            print(pixel, end="")
        print("")


class Image:
    def __init__(self, contents, algorithm):
        self.contents = contents
        self.default = 0
        self.algorithm = algorithm

    def enhance(self):
        (min_x, max_x), (min_y, max_y) = self.size
        self.contents = {
            (x, y): self.get_new_pixel((x, y))
            for x in range(min_x - 1, max_x + 2)
            for y in range(min_y - 1, max_y + 2)
        }
        self.default = self.get_new_pixel((inf, inf))

    def get_new_pixel(self, coords):
        neighbours = self.get_neighbours(coords)
        index = int("".join(map(str, neighbours)), 2)
        return 1 if self.algorithm[index] == "#" else 0

    @property
    def size(self):
        return get_image_size(self.contents)

    @property
    def lit_pixels(self):
        return list(self.contents.values()).count(1)

    def get_neighbours(self, coords):
        x, y = coords
        directions = [
            (x - 1, y - 1),
            (x, y - 1),
            (x + 1, y - 1),
            (x - 1, y),
            (x, y),
            (x + 1, y),
            (x - 1, y + 1),
            (x, y + 1),
            (x + 1, y + 1),
        ]
        return [self.contents.get(coords, self.default) for coords in directions]


@utils.profile
def part1(raw: str):
    algorithm, image = init(raw)
    image = Image(image, algorithm)
    for _ in range(2):
        image.enhance()
    return image.lit_pixels


@utils.profile
def part2(raw: str):
    algorithm, image = init(raw)
    image = Image(image, algorithm)
    for _ in range(50):
        image.enhance()
    return image.lit_pixels


if __name__ == "__main__":
    raw = utils.load_puzzle_input("2021/day20")
    assert part1(raw) == 5225
    assert part2(raw) == 18131
