from abc import ABC, abstractmethod
from typing import Literal

from src.common import Dimensions, Move, SweeperConfiguration
from src.game.grids import Grid
from src.game.tiles import Tile

Result = Literal['VICTORY', 'FAILURE']

GameState = Literal[Result, 'IN_PROGRESS']
"""
  - `IN_PROGRESS` - game is in progress even when it's not started
  - `VICTORY` - game is over - all mines have been correctly flagged
  - `FAILURE` - uncovered tiles with a mine
"""


class Sweeper[C: SweeperConfiguration](ABC):
    def __init__(self, configuration: C) -> None:
        self._configuration = configuration

        # TODO: check mine count - if it makes sense or not

    def get_dimensions(self) -> Dimensions:
        return self._configuration.dimensions

    def _check_grid_size(self, grid: Grid[Tile]) -> None:
        if grid.get_width() != self._configuration.dimensions.width:
            raise ValueError('Grid dimensions (width) do not match')
        elif grid.get_height() != self._configuration.dimensions.height:
            raise ValueError('Grid dimensions (height) do not match')

    @abstractmethod
    def obtain_remaining_mines(self) -> int:  # TODO: could be implemented, right here, right? do I want it tho?
        ...

    @abstractmethod
    def obtain_state(self) -> GameState:
        ...

    @abstractmethod
    def obtain_time(self) -> int:
        ...

    @abstractmethod
    def obtain_grid[T: Tile](self, old_grid: Grid[T] | None = None) -> Grid[T]:
        ...

    @abstractmethod
    def play(self, move: Move) -> None:
        ...

    @abstractmethod
    def reset(self) -> None:
        ...

    @abstractmethod
    def sign_victory(self, name: str) -> None:
        ...
