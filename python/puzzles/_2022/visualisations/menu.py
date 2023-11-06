from typing import TYPE_CHECKING, Callable

from pygame import Color
from pygame.surface import Surface
from robingame.animation import ease_out
from robingame.gui import Button, Menu
from robingame.objects import Entity, Group
from robingame.text.font import fonts

from puzzles._2022.visualisations import day14sand, day5columns, day8trees, day9rope

if TYPE_CHECKING:
    from puzzles._2022.visualisations.game import Advent2022Visualisations


class Button(Button):
    animation_duration = 20

    def __init__(
        self,
        x: int,
        y: int,
        width: int = 300,
        height: int = 50,
        text=None,
        on_press=None,
        on_focus=None,
        on_release=None,
        on_unfocus=None,
    ):
        self.start_y = -50
        self.start_x = -50
        self.target_x = x
        self.target_y = y
        super().__init__(
            self.start_x,
            self.start_y,
            width,
            height,
            text,
            on_press,
            on_focus,
            on_release,
            on_unfocus,
        )
        self.image = Surface((width, height))
        self.image.fill(Color("white"))
        fonts.cellphone_black.render(
            surf=self.image,
            text=self.text,
            wrap=width,
            align=0,
            scale=2,
        )
        self.state = self.state_animate_in

    def state_animate_in(self):
        self.y = ease_out(
            self.tick, start=self.start_y, stop=self.target_y, num=self.animation_duration
        )
        self.x = ease_out(
            self.tick, start=self.start_x, stop=self.target_x, num=self.animation_duration
        )
        if self.tick == self.animation_duration - 1:
            self.state = self.state_idle


class AdventVizMenu(Menu):
    game: "Advent2022Visualisations"

    def __init__(self):
        super().__init__()
        self.buttons = Group()
        self.child_groups = [self.buttons]
        visualisations = {
            "day5 (columns) part 1": day5columns.Day5Part1Visualisation,
            "day5 (columns) part 2": day5columns.Day5Part2Visualisation,
            "day8 (trees) part 1": day8trees.Day8Part1Visualisation,
            "day8 (trees) part 2": day8trees.Day8Part2Visualisation,
            "day9 (rope) part 1": day9rope.Day9Part1Visualisation,
            "day9 (rope) part 2": day9rope.Day9Part2Visualisation,
            "day14 (sand) part 1": day14sand.Day14Part1Visualisation,
            "day14 (sand) part 2": day14sand.Day14Part2Visualisation,
        }
        for ii, (label, entity) in enumerate(visualisations.items()):
            y_spacing = 100
            self.buttons.add(
                Button(
                    x=200,
                    y=y_spacing * ii + 100,
                    text=label,
                    on_press=self.create_on_press(entity, label),
                )
            )

    def create_on_press(self, entity: type[Entity], label: str) -> Callable:
        def on_press(button):
            self.exit()
            self.game.scenes.add(entity())
            print(f"clicked for {label}")

        return on_press

    def exit(self):
        for group in self.child_groups:
            for entity in group:
                if hasattr(entity, "exit"):
                    entity.exit()
                else:
                    entity.kill()
        self.state = self.state_exit

    def state_exit(self):
        """Die when all entities have finished animating out"""
        if not any(self.child_groups):
            self.kill()
