import sys

import pygame
from robingame.input import EventQueue
from robingame.objects import Game

from python._2022.visualisations import day14sand


class Advent2022Visualisations(Game):
    window_caption = "Advent of Code 2022"
    window_width = 1000
    window_height = 1000
    fps = 0  # run as fast as possible
    ticks_per_frame = 1

    def __init__(self):
        super().__init__()
        self.scenes.add(day14sand.Day14Part2Visualisation())

    def update(self):
        for _ in range(self.ticks_per_frame):
            super().update()

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
