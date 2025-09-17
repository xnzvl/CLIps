from typing import Set, override
from random import randint

from src.common import Move, Point, SweeperConfiguration
from src.game.grids.grid import Grid
from src.game.grids.impl.passive_grid import PassiveGrid
from src.game.sweeper.sweeper import GameState, Sweeper


class Minefield(Sweeper):
    def __init__(self, configuration: SweeperConfiguration) -> None:
        super().__init__(configuration)

        self._start_time: int | None = None
        self._field: Grid = PassiveGrid(self._configuration.dimensions)

    def _plant_mines(self, safe_spot: Point) -> None:
        dimensions = self._configuration.dimensions
        planted_mines: Set[Point] = set()

        for m in range(self._configuration.mines):
            new_mine = Point(
                randint(0, dimensions.width - 1),
                randint(0, dimensions.height - 1)
            )

            if safe_spot != new_mine and new_mine not in planted_mines:
                continue

            planted_mines.add(new_mine)
            # TODO: plant onto the field

    @override
    def obtain_remaining_mines(self) -> int:
        pass

    @override
    def obtain_state(self) -> GameState:
        pass

    @override
    def obtain_time(self) -> int:
        pass

    @override
    def obtain_grid(self, old_grid: Grid | None = None) -> Grid:
        pass

    @override
    def play(self, move: Move) -> None:
        # TODO: implement

        if self._start_time is None:
            self._plant_mines(move.tile)

    @override
    def reset(self) -> None:
        self._start_time = None
        self._field = PassiveGrid(self._configuration.dimensions)

    @override
    def sign_victory(self, name: str) -> None:
        pass
