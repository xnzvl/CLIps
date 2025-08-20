from abc import ABC, abstractmethod
from typing import List

from src.common import Move
from src.game.grids.grid import Grid


class Strategy(ABC):
    @abstractmethod
    def get_moves(self, grid: Grid) -> List[Move]:
        ...
