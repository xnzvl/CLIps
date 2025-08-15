from itertools import combinations
from typing import List, Tuple

from src.common import Move, Point
from src.exceptions import InvalidGameStateError
from src.game.grids.grid import Grid
from src.game.grids.impl.mutable_grid import MutableGrid
from src.game.tiles.tile import Tile


def _all_possible_flag_scenarios(grid: Grid, point: Point, tile: Tile) -> List[List[Tuple[Point, Tile]]]:
    scenarios: List[List[Tuple[Point, Tile]]] = list()

    mine_count = tile.get_count()
    assert mine_count is not None

    max_to_be_flagged = mine_count - grid.count_symbol_in_neighbourhood(point.x, point.y, 'FLAG')
    if max_to_be_flagged < 0:
        raise InvalidGameStateError('too many flagged tiles')

    for potential_flags in range(max_to_be_flagged, 0, -1):
        for indices in combinations(
                grid.get_neighbours_with_symbol(point.x, point.y, 'COVERED', 'QUESTION_MARK'),
                potential_flags
        ):
            scenarios.append(list(indices))

    return scenarios


def _simulate_around(grid: Grid, number_point: Point) -> List[Move] | None:

    return list()


def calculate_safe_moves(grid: Grid) -> List[Move]:
    for point, tile in grid:
        if tile.get_symbol() != 'NUMBER':
            continue

        flag_options = grid.get_neighbours_of_tile_at(point.x, point.y)

    return list()


def main() -> None:
    simple_grid = MutableGrid(5, 2)
    for x in range(5):
        simple_grid[x, 1].set_count(1 if x != 1 and x != 3 else 2)

    simple_grid.print()


    trickier_grid = MutableGrid(4, 3)
    trickier_grid[0, 1].set_count(1)
    trickier_grid[1, 1].set_count(1)
    trickier_grid[2, 1].set_count(3)
    trickier_grid[0, 2].set_count(0)
    trickier_grid[1, 2].set_count(0)
    trickier_grid[2, 2].set_count(1)

    trickier_grid.print()

    print()
    return


if __name__ == '__main__':
    main()
