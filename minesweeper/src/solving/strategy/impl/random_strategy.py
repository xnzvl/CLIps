from typing import List

from src.common import Move
from src.game.grids.impl.mutable_grid import MutableGrid
from src.solving.strategy.steps import random_move
from src.solving.strategy.strategy import Strategy


class RandomStrategy(Strategy):
    def get_moves(self, board: MutableGrid) -> List[Move]:
        return random_move(board)
