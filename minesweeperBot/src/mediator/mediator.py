from abc import ABC, abstractmethod

from src.common import Configuration, Dimensions, Move, Point
from src.game.board import Board
from src.game.literals import GameState


class Mediator(ABC):
    def __init__(self, configuration: Configuration) -> None:
        self._dimensions = configuration.dimensions
        self._offsets = configuration.offsets

    def get_dimensions(self) -> Dimensions:
        return self._dimensions

    def get_offsets(self) -> Point:
        return self._offsets

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

    @abstractmethod
    def play(self, move: Move) -> None:
        ...

    @abstractmethod
    def reset(self) -> None:
        ...

    @abstractmethod
    def post_game_procedure(self) -> None:
        ...
