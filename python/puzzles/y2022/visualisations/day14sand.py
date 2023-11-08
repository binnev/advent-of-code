from pygame import Surface, Color
from robingame.image import scale_image
from robingame.objects import Entity
from robingame.text.font import fonts

import utils
from puzzles.y2022.day14 import parse_input, DESTROYED, sand_trace, SAND, WALL


class Day14Part1Visualisation(Entity):
    def __init__(self):
        super().__init__()
        input = utils.load_puzzle_input("2022/day14")
        self.grid = parse_input(input)
        self.origin = (500, 0)
        self.floor = max(y for x, y in self.grid)
        self.ii = 0
        self.state = self.state_main

    def state_main(self):
        status = sand_trace(
            self.origin,
            self.grid,
            floor=self.floor,
            solid_floor=False,
        )
        if status == DESTROYED:
            self.state = self.state_idle
            return
        self.ii += 1

    def state_idle(self):
        pass

    def draw(self, surface: Surface, debug: bool = False):
        super().draw(surface, debug)
        xmin, xmax = self.grid.get_xlim()
        ymin, ymax = self.grid.get_ylim()
        width = xmax - xmin + 1 + 20
        height = ymax - ymin + 1 + 20
        x_offset = -xmin + 10
        y_offset = -ymin + 10
        image = Surface((width, height))
        image.fill(Color("white"))
        for (x, y), value in self.grid.items():
            coord = (x + x_offset, y + y_offset)
            mapping = {
                SAND: Color("orange"),
                WALL: Color("black"),
            }
            color = mapping[value]
            image.set_at(coord, color)
        fonts.cellphone_black.render(
            surf=image,
            text=f"Sand grains: {self.ii}",
            wrap=width,
            align=0,
            scale=1,
        )
        x_scale = surface.get_width() / image.get_width()
        y_scale = surface.get_height() / image.get_height()
        scale = min(x_scale, y_scale)
        image = scale_image(image, scale)
        x = (surface.get_width() - image.get_width()) / 2
        surface.blit(image, (x, 0))


class Day14Part2Visualisation(Day14Part1Visualisation):
    def __init__(self):
        super().__init__()
        input = utils.load_puzzle_input("2022/day14")
        self.grid = parse_input(input)
        self.origin = (500, 0)
        self.floor = 2 + max(y for x, y in self.grid)
        self.ii = 0
        self.state = self.state_main

    def state_main(self):
        sand_trace(self.origin, self.grid, floor=self.floor, solid_floor=True)
        self.ii += 1
        if self.origin in self.grid:
            self.state = self.state_idle
            return

    def state_idle(self):
        pass
