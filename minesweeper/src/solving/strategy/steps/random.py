from random import choice
from typing import List

from src.common import Move
from src.game.grids.grid import Grid


def random_move(grid: Grid, covered_only: bool = True) -> List[Move]:
    random_moves: List[List[Move]] = list()

    for point, tile in grid:
        symbol = tile.get_symbol()

        if symbol == 'COVERED':
            random_moves.append([Move('primary', point)])
        elif not covered_only and (symbol == 'FLAG' or symbol == 'QUESTION_MARK'):
            random_moves.append([Move('secondary', point), Move('primary', point)])

    return choice(random_moves) if len(random_moves) > 0 else []

# TODO: less random -> pick a tile from edge
