import matplotlib
import numpy
import pygame
from pygame import Surface, Color
from robingame.image import scale_image
from robingame.input import EventQueue
from robingame.objects import Entity
from robingame.text.font import fonts

from python import utils
from python._2022.day9 import move_head, move_tail
from python.utils import SparseMatrix


class Day9Part1Visualisation(Entity):
    def __init__(self):
        super().__init__()
        input = utils.load_puzzle_input("2022/day9")
        self.instructions = input.splitlines()
        self.head = (0, 0)
        self.tail = (0, 0)
        self.tail_history = {self.tail}
        self.ii = 0
        num_colours = 3
        samples = numpy.linspace(0, 1, num_colours)
        self.colours = {
            ii: tuple(map(int, color[:3]))
            for ii, color in enumerate(matplotlib.cm.viridis(samples) * 256)
        }
        self.state = self.state_main

    def update(self):
        super().update()
        for event in EventQueue.events:
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_SPACE:
                        self.__init__()

    def state_main(self):
        try:
            instruction = self.instructions[self.ii]
        except IndexError:
            self.state = self.state_idle
            return

        direction, amount = instruction.split()
        amount = int(amount)
        for _ in range(amount):
            self.head = move_head(self.head, direction)
            self.tail = move_tail(self.head, self.tail)
            self.tail_history.add(self.tail)
        self.ii += 1

    def state_idle(self):
        pass

    def draw(self, surface: Surface, debug: bool = False):
        super().draw(surface, debug)
        grid = SparseMatrix()
        for coord in self.tail_history:
            grid[coord] = 0
        grid[self.tail] = 1
        grid[self.head] = 2

        xmin, xmax = grid.get_xlim()
        ymin, ymax = grid.get_ylim()
        width = xmax - xmin + 1 + 20
        height = ymax - ymin + 1 + 20
        x_offset = -xmin + 10
        y_offset = -ymin + 10
        image = Surface((width, height))
        image.fill(Color("white"))
        for (x, y), value in grid.items():
            coord = (x + x_offset, y + y_offset)
            color = self.colours[value]
            image.set_at(coord, color)
        x_scale = surface.get_width() / image.get_width()
        y_scale = surface.get_height() / image.get_height()
        scale = min(x_scale, y_scale)
        image = scale_image(image, scale)
        fonts.cellphone_black.render(
            surf=image,
            text=f"tail history = {len(self.tail_history)}",
            wrap=width*scale,
            align=0,
            scale=2,
        )
        x = (surface.get_width() - image.get_width()) / 2
        surface.blit(image, (x, 0))
