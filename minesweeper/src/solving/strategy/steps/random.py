from random import choice
from typing import List

from src.common import Move
from src.game.grids.grid import Grid


def random_move(grid: Grid) -> List[Move]:  # TODO: more customizable! (only edge ones, only COVERED)
    random_moves: List[Move] = list()

    for point, tile in grid:
        if not tile.is_covered():
            continue

        random_moves.append(Move('UNCOVER', point))

    return [choice(random_moves)] if len(random_moves) > 0 else list()
