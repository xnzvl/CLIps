from abc import ABC, abstractmethod
from typing import List

from src.common import Move
from src.game.grids.grid import Grid
from src.game.tiles import Tile


class Strategy(ABC):
    @abstractmethod
    def get_moves[T: Tile](self, grid: Grid[T]) -> List[Move]:
        ...
