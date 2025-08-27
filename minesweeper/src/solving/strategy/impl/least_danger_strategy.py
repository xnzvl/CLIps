from random import choice
from typing import List

from src.common import Move
from src.game.grids.grid import Grid
from src.solving.strategy.steps.certain import certain_flags, certain_safe_moves
from src.solving.strategy.steps.educated import least_danger_moves
from src.solving.strategy.strategy import Strategy


class LeastDangerStrategy(Strategy):
    def get_moves(self, grid: Grid) -> List[Move]:
        certain_moves = certain_flags(grid)
        certain_moves.extend(certain_safe_moves(grid))

        if len(certain_moves) > 0:
            return certain_moves

        least_danger = least_danger_moves(grid)

        return [choice(least_danger)]
