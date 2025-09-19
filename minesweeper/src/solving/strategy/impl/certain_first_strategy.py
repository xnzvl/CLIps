from typing import List

from src.common import Move
from src.game.grids import Grid
from src.game.tiles import Tile
from src.solving.strategy.steps.certain import certain_flags, certain_safe_moves
from src.solving.strategy.steps.random import random_move
from src.solving.strategy.strategy import Strategy


class CertainFirstStrategy(Strategy):
    def get_moves[T: Tile](self, grid: Grid[T]) -> List[Move]:
        certain_moves = certain_flags(grid)
        certain_moves.extend(certain_safe_moves(grid))

        return certain_moves \
            if len(certain_moves) > 0 \
            else random_move(grid)
