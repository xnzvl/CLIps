from abc import ABC, abstractmethod
from typing import List

from src.common import Move
from src.game.grids.impl.mutable_grid import MutableGrid


class Strategy(ABC):
    # TODO: really a mutable grid here? is it necessary?
    @abstractmethod
    def get_moves(self, board: MutableGrid) -> List[Move]:
        ...
