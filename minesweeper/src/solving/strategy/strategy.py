from abc import ABC, abstractmethod
from typing import List

from src.common import Move
from src.game.grids import Grid
from src.game.tiles import Tile


class Strategy(ABC):
    @abstractmethod
    def apply[T: Tile](self, grid: Grid[T]) -> List[Move]:
        ...
