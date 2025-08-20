from typing import List

from src.common import Move
from src.game.grids.grid import Grid
from src.solving.strategy.steps.calculated import calculate_safe_moves
from src.solving.strategy.steps.certain import certain_flags, certain_safe_moves
from src.solving.strategy.steps.random import random_move
from src.solving.strategy.strategy import Strategy


class CalculatedStrategy(Strategy):
    def get_moves(self, grid: Grid) -> List[Move]:
        certain_moves = certain_flags(grid)
        certain_moves.extend(certain_safe_moves(grid))

        if len(certain_moves) == 0:
            certain_moves.extend(calculate_safe_moves(grid))
            print(f'  CALCULATED SAFE MOVES: {certain_moves}')
            if len(certain_moves) == 0:
                print('    NO LUCK -> TIME TO GUESS')

        return certain_moves \
            if len(certain_moves) > 0 \
            else random_move(grid)
