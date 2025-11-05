from typing import List

from src.common import Move
from src.game.grids import Grid
from src.game.tiles import Tile
from src.solving.strategy import Strategy


class ForesightStep(Strategy):
    def apply[T: Tile](self, grid: Grid[T]) -> List[Move]:  # TODO: implement
        return list()
