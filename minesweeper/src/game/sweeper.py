from abc import ABC, abstractmethod
from typing import Literal, Union

from src.common import Configuration, Dimensions, Move, Point
from src.game.grids.grid import Grid


Result = Literal['VICTORY', 'FAILURE']

GameState = Union[Result, Literal['IN_PROGRESS']]
"""
  - `IN_PROGRESS` - game is in progress even when it's not started
  - `VICTORY` - game is over - all mines have been correctly flagged
  - `FAILURE` - uncovered tiles with a mine
"""


class Sweeper(ABC):
    def __init__(self, configuration: Configuration) -> None:
        self._dimensions = configuration.dimensions
        self._offsets = configuration.offsets

    def get_dimensions(self) -> Dimensions:
        return self._dimensions

    def get_offsets(self) -> Point:
        return self._offsets

    def _check_grid_size(self, grid: Grid) -> None:
        if grid.get_width() != self._dimensions.width:
            raise ValueError('Grid dimensions (width) do not match')
        elif grid.get_height() != self._dimensions.height:
            raise ValueError('Grid dimensions (height) do not match')

    @abstractmethod
    def obtain_remaining_mines(self) -> int:
        ...

    @abstractmethod
    def obtain_state(self) -> GameState:
        ...

    @abstractmethod
    def obtain_time(self) -> int:
        ...

    @abstractmethod
    def obtain_grid(self, old_grid: Grid | None = None) -> Grid:
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
