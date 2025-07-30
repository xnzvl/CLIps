from abc import ABC, abstractmethod
from typing import List

from src.common import Move
from src.game.board import Board


class Strategy(ABC):
    @abstractmethod
    def get_moves(self, board: Board) -> List[Move]:
        ...
