from abc import ABC, abstractmethod

from src.common import Configuration, Dimensions, Point
from src.game.board import Board
from src.game.game import Game, GameState


class Observer(ABC):
    def __init__(self, configuration: Configuration) -> None:
        self._offsets = configuration.offsets
        self._dimensions = configuration.dimensions

    def get_offsets(self) -> Point:
        return self._offsets

    def get_dimensions(self) -> Dimensions:
        return self._dimensions

    def observe_game(self, old_board: Board | None = None) -> Game:
        return Game(self.observe_board(old_board), self.observe_state())

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
