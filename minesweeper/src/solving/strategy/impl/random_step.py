from random import choice
from typing import List, override

from src.common import Action, Move
from src.game.grids import Grid
from src.game.tiles import Tile

from ..strategy import Strategy


class RandomStep(Strategy):  # TODO: more customizable! (only edge ones, only COVERED)
    @override
    def apply[T: Tile](self, grid: Grid[T]) -> List[Move]:
        random_moves: List[Move] = list()

        for point, tile in grid:
            if not tile.is_covered():
                continue

            random_moves.append(Move(Action.UNCOVER, point))

        return [choice(random_moves)] if len(random_moves) > 0 else list()
