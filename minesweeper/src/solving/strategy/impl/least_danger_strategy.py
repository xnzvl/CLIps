from random import choice
from typing import List

from src.common import Move
from src.game.grids.impl.mutable_grid import MutableGrid
from src.solving.strategy.steps.certain import certain_flags, certain_safe_moves
from src.solving.strategy.steps.educated import least_danger_moves
from src.solving.strategy.strategy import Strategy


class LeastDangerStrategy(Strategy):
    def get_moves(self, board: MutableGrid) -> List[Move]:
        certain_moves = certain_flags(board)
        certain_moves.extend(certain_safe_moves(board))

        if len(certain_moves) > 0:
            return certain_moves

        least_danger = least_danger_moves(board)

        return [choice(least_danger)]
