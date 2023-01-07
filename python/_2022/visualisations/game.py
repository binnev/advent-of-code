import sys

import pygame
from pygame.surface import Surface
from robingame.input import EventQueue
from robingame.objects import Game
from robingame.text.font import fonts

from python._2022.visualisations import day14sand, day5columns


class Advent2022Visualisations(Game):
    window_caption = "Advent of Code 2022"
    window_width = 1000
    window_height = 1000
    fps = 60  # run as fast as possible
    ticks_per_frame = 1

    def __init__(self):
        super().__init__()
        self.scenes.add(day5columns.Day5Part2Visualisation())

    def update(self):
        for _ in range(self.ticks_per_frame):
            super().update()

    def draw(self, surface: Surface, debug: bool = False):
        super().draw(surface, debug)
        text = "\n".join(
            [
                f"iterations: {self.tick}",
                f"ticks per frame: {self.ticks_per_frame}",
                f"fps: {self.fps}",
            ]
        )
        fonts.cellphone_white.render(surface, text, scale=2)

    def read_inputs(self):
        super().read_inputs()
        for event in EventQueue.events:
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    case pygame.K_DOWN:
                        self.ticks_per_frame = max([1, self.ticks_per_frame // 2])
                    case pygame.K_UP:
                        self.ticks_per_frame *= 2
                    case pygame.K_RIGHT:
                        self.fps *= 2
                    case pygame.K_LEFT:
                        self.fps = max(1, self.fps // 2)


if __name__ == "__main__":
    Advent2022Visualisations().main()
