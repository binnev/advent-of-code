import pygame
from pygame import Surface, Color
from robingame.image import scale_image
from robingame.input import EventQueue
from robingame.objects import Entity
from robingame.text.font import fonts

import utils
from solutions._2022.day5 import parse_input, move


class Day5Part1Visualisation(Entity):
    def __init__(self):
        super().__init__()
        input = utils.load_puzzle_input("2022/day5")
        self.columns, self.instructions = parse_input(input)
        self.ii = 0
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
            amount, origin, destination = self.instructions[self.ii]
        except IndexError:
            self.state = self.state_idle
            return
        for _ in range(amount):
            move(origin, destination, self.columns)
        self.ii += 1

    def state_idle(self):
        pass

    def draw(self, surface: Surface, debug: bool = False):
        super().draw(surface, debug)
        letter_height = 9
        letter_width = 7
        rpad = 1
        height = letter_height * max(len(column) + 1 for index, column in self.columns.items())
        width = letter_width * len(self.columns)
        image = Surface((width, height))
        image.fill(Color("white"))
        h_spacing = letter_width
        for index, column in self.columns.items():
            characters = column[::-1] + str(index)
            col_height = len(characters) * letter_height
            x = (index - 1) * h_spacing + rpad
            y = height - col_height
            fonts.cellphone_black.render(surf=image, text="\n".join(characters), x=x, y=y)
        x_scale = surface.get_width() / image.get_width()
        y_scale = surface.get_height() / image.get_height()
        scale = min(x_scale, y_scale)
        image = scale_image(image, scale)
        try:
            amount, origin, destination = self.instructions[self.ii]
            text = f"move {amount} from {origin} to {destination}"
        except IndexError:
            result = "".join(self.columns[key][-1] for key in sorted(self.columns.keys()))
            text = f"done.\n{result=}"

        fonts.cellphone_black.render(
            surf=image,
            text=text,
            wrap=image.get_width(),
            align=0,
            scale=2,
        )
        x = (surface.get_width() - image.get_width()) / 2
        surface.blit(image, (x, 0))


class Day5Part2Visualisation(Day5Part1Visualisation):
    def state_main(self):
        try:
            amount, origin, destination = self.instructions[self.ii]
        except IndexError:
            self.state = self.state_idle
            return
        move(origin, destination, self.columns, amount=amount)
        self.ii += 1
