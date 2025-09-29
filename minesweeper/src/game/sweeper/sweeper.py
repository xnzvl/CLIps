from abc import ABC, abstractmethod

from src.common import Move, SweeperConfiguration, Dimensioned
from src.game.grids import Grid
from src.game.sweeper import GameState, SweeperError
from src.game.tiles import Tile


class Sweeper[C: SweeperConfiguration](Dimensioned, ABC):
    def __init__(self, configuration: C) -> None:
        super().__init__(configuration.dimensions)

        self._configuration = configuration

        dimensions = self._configuration.dimensions
        total_tiles = dimensions.width * dimensions.height

        if total_tiles <= configuration.mines:
            raise SweeperError(
                'too many mines - ' +
                f'required mines: {configuration.mines}, total tiles: {total_tiles}'
            )

    def _check_grid_size[T: Tile](self, grid: Grid[T]) -> None:
        if grid.get_width() != self._configuration.dimensions.width:
            raise ValueError('Grid dimensions (width) do not match')
        if grid.get_height() != self._configuration.dimensions.height:
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
    def obtain_grid(self, old_grid: Grid[Tile] | None = None) -> Grid[Tile]:
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
