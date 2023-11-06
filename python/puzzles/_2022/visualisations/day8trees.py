import matplotlib
import numpy
import pygame
from pygame import Surface, Color
from robingame.image import scale_image
from robingame.input import EventQueue
from robingame.objects import Entity
from robingame.text.font import fonts

import utils
from puzzles._2022.day8 import parse_input, scenic_score, is_visible_2d


class Day8Part1Visualisation(Entity):
    def __init__(self):
        super().__init__()
        input = utils.load_puzzle_input("2022/day8")
        self.grid = parse_input(input)
        self.ii = self.x = self.y = 0
        self.score = 0
        self.state = self.state_main
        num_colours = 10
        samples = numpy.linspace(0, 1, num_colours)
        self.colours = {
            ii: tuple(map(int, color[:3]))
            for ii, color in enumerate(matplotlib.cm.viridis(samples) * 256)
        }
        self.visible = []

    def update(self):
        super().update()
        for event in EventQueue.events:
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_SPACE:
                        self.__init__()

    def state_main(self):
        w, h = self.grid.shape
        if self.ii == w * h:
            self.state = self.state_idle
            return

        self.x, self.y = divmod(self.ii, len(self.grid))
        if is_visible_2d(x=self.x, y=self.y, grid=self.grid):
            self.score += 1
            self.visible.append((self.x, self.y))

        self.ii += 1

    def state_idle(self):
        pass

    def draw(self, surface: Surface, debug: bool = False):
        super().draw(surface, debug)
        width, height = self.grid.shape
        image = Surface((width, height))
        image.fill(Color("white"))
        for y, row in enumerate(self.grid):
            for x, value in enumerate(row):
                color = self.colours[value]
                image.set_at((x, y), color)

        image.set_at((self.x, self.y), Color("white"))
        for coord in self.visible:
            image.set_at(coord, Color("red"))
        x_scale = surface.get_width() / image.get_width()
        y_scale = surface.get_height() / image.get_height()
        scale = min(x_scale, y_scale)
        image = scale_image(image, scale)
        fonts.cellphone_black.render(
            surf=image,
            text=f"visible trees = {self.score}",
            wrap=width * scale,
            align=0,
            scale=4,
        )
        x = (surface.get_width() - image.get_width()) / 2
        surface.blit(image, (x, 0))


class Day8Part2Visualisation(Day8Part1Visualisation):
    def __init__(self):
        super().__init__()
        self.record_holder = (0, 0)

    def state_main(self):
        w, h = self.grid.shape
        if self.ii == w * h:
            self.state = self.state_idle
            return

        self.x, self.y = divmod(self.ii, len(self.grid))
        score = scenic_score(self.x, self.y, self.grid)
        if score > self.score:
            self.score = score
            self.record_holder = (self.x, self.y)

        self.ii += 1

    def state_idle(self):
        pass

    def draw(self, surface: Surface, debug: bool = False):
        super().draw(surface, debug)
        width, height = self.grid.shape
        image = Surface((width, height))
        image.fill(Color("white"))
        rec_x, rec_y = self.record_holder
        for y, row in enumerate(self.grid):
            for x, value in enumerate(row):
                color = self.colours[value]
                if x == rec_x or y == rec_y:
                    color = Color("orange")
                image.set_at((x, y), color)

        image.set_at((self.x, self.y), Color("white"))
        image.set_at(self.record_holder, Color("red"))

        x_scale = surface.get_width() / image.get_width()
        y_scale = surface.get_height() / image.get_height()
        scale = min(x_scale, y_scale)
        image = scale_image(image, scale)
        fonts.cellphone_black.render(
            surf=image,
            text=f"most scenic tree score = {self.score}",
            wrap=width * scale,
            align=0,
            scale=4,
        )
        x = (surface.get_width() - image.get_width()) / 2
        surface.blit(image, (x, 0))
