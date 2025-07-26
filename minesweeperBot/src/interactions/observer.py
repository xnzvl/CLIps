from abc import ABC, abstractmethod

from src.common import Configuration, Dimensions, Game, GameState, Point
from src.game.board import Board


class Observer(ABC):
    def __init__(self, configuration: Configuration) -> None:
        self._offsets = configuration.offsets
        self._dimensions = configuration.dimensions
        self._tile_size = configuration.tile_size

    def get_offsets(self) -> Point:
        return self._offsets

    def get_dimensions(self) -> Dimensions:
        return self._dimensions

    def get_tile_size(self) -> int:
        return self._tile_size

    def observe_game(self) -> Game:
        return Game(self.observe_board(), self.observe_state())

    def _check_board_size(self, board: Board) -> None:
        if board.get_width() != self._dimensions.width:
            raise ValueError('Board dimensions (width) do not match')
        elif board.get_height() != self._dimensions.height:
            raise ValueError('Board dimensions (height) do not match')

    @abstractmethod
    def observe_state(self) -> GameState:
        ...

    @abstractmethod
    def observe_board(self, old_board: Board | None = None) -> Board:
        ...
