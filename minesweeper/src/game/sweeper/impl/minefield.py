from typing import Set, override

from src.common import Move, Point, SweeperConfiguration
from src.game.grids.grid import Grid
from src.game.sweeper.sweeper import GameState, Sweeper


class Minefield(Sweeper):
    def __init__(self, configuration: SweeperConfiguration) -> None:
        super().__init__(configuration)

        self._mines: Set[Point] = set()

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
        pass

    @override
    def sign_victory(self, name: str) -> None:
        pass
