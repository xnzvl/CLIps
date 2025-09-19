from typing import List

from src.common import Move
from src.game.grids import Grid
from src.game.tiles import Tile
from src.solving.strategy.steps.random import random_move
from src.solving.strategy.strategy import Strategy


class RandomStrategy(Strategy):
    def get_moves[T: Tile](self, grid: Grid[T]) -> List[Move]:
        return random_move(grid)
