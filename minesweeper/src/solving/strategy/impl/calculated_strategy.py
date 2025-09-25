from typing import List

from src.common import Move
from src.game.grids import Grid
from src.game.tiles import Tile
from src.solving.strategy.impl.calculated import calculate_safe_moves
from src.solving.strategy.steps.impl.certain_step import certain_flags, certain_uncovers
from src.solving.strategy.steps.impl.random_step import random_move
from src.solving.strategy.strategy import Strategy


class CalculatedStrategy(Strategy):
    def get_moves[T: Tile](self, grid: Grid[T]) -> List[Move]:
        certain_moves = certain_flags(grid)
        certain_moves.extend(certain_uncovers(grid))

        if len(certain_moves) == 0:
            certain_moves.extend(calculate_safe_moves(grid))
            print(f'  CALCULATED SAFE MOVES: {certain_moves}')
            if len(certain_moves) == 0:
                print('    NO LUCK -> TIME TO GUESS')

        return certain_moves \
            if len(certain_moves) > 0 \
            else random_move(grid)
