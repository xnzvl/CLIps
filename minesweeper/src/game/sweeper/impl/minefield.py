from typing import Set, override

from src.common import Move, Point, SweeperConfiguration
from src.game.grids.grid import Grid
from src.game.grids.impl.generic_grid import GenericGrid
from src.game.sweeper.sweeper import GameState, Sweeper


class Minefield(Sweeper):
    def __init__(self, configuration: SweeperConfiguration) -> None:
        super().__init__(configuration)

        self._start_time = None
        self._mines: Set[Point] = set()
        self._field = self._new_field()

    def _new_field(self) -> Grid:
        return GenericGrid(self._configuration.dimensions)

    def _plant_mines(self, safe_spot: Point) -> None:
        pass

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
        pass

    @override
    def reset(self) -> None:
        self._mines.clear()
        self._field = self._new_field()

    @override
    def sign_victory(self, name: str) -> None:
        pass
