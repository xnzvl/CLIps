from abc import ABC, abstractmethod
from typing import Literal, Union

from src.common import Dimensions, Move
from src.game.grids.grid import Grid


Result = Literal['VICTORY', 'FAILURE']

GameState = Union[Result, Literal['IN_PROGRESS']]
"""
  - `IN_PROGRESS` - game is in progress even when it's not started
  - `VICTORY` - game is over - all mines have been correctly flagged
  - `FAILURE` - uncovered tiles with a mine
"""


class Sweeper(ABC):
    def __init__(self, dimensions: Dimensions) -> None:
        self._dimensions = dimensions

    def get_dimensions(self) -> Dimensions:
        return self._dimensions

    def _check_grid_size(self, grid: Grid) -> None:
        if grid.get_width() != self._dimensions.width:
            raise ValueError('Grid dimensions (width) do not match')
        elif grid.get_height() != self._dimensions.height:
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
