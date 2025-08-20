from typing import List

from src.common import Move
from src.game.grids.grid import Grid
from src.solving.strategy.steps.random import random_move
from src.solving.strategy.strategy import Strategy


class RandomStrategy(Strategy):
    def get_moves(self, grid: Grid) -> List[Move]:
        return random_move(grid)
