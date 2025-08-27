from abc import ABC, abstractmethod

from src.common import Configuration, Dimensions, Move, Point
from src.game.grids.grid import Grid
from src.game.literals import GameState


class Mediator(ABC):
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
    def observe_state(self) -> GameState:
        ...

    @abstractmethod
    def observe_grid(self, old_grid: Grid | None = None) -> Grid:
        ...

    @abstractmethod
    def play(self, move: Move) -> None:
        ...

    @abstractmethod
    def reset(self) -> None:
        ...

    def post_game_procedure(self) -> None:
        return
