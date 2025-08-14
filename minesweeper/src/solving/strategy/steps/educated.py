from functools import reduce
from typing import Dict, List, Tuple

from src.common import Move, Point
from src.game.grids.grid import Grid
from src.game.tiles.tile import Tile


def _flag_reducer(accumulator: int, t: Tuple[Point, Tile]) -> int:
    _, tile = t
    return (accumulator + 1) if tile.get_symbol() == 'FLAG' else accumulator


def _assess_danger_levels(grid: Grid) -> Dict[Point, Tuple[int, int]]:
    danger_levels: Dict[Point, Tuple[int, int]] = dict()

    for point, tile in grid:
        if tile.get_symbol() != 'NUMBER':
            continue

        neighbours = grid.get_neighbours_of_tile_at(point.x, point.y)
        flags = reduce(_flag_reducer, neighbours, 0)

        count = tile.get_count()
        assert count is not None
        if flags > count:
            raise RuntimeError('invalid state - too many flags')

        danger_increase = 1 if flags < count else 0
        for n_point, n_tile in neighbours:
            symbol = n_tile.get_symbol()
            if symbol == 'COVERED' or symbol == 'QUESTION_MARK':
                danger_lvl, max_danger = danger_levels.get(n_point, (0, 0))
                danger_levels[n_point] = (danger_lvl + danger_increase, max_danger + 1)

    return danger_levels


def least_danger_moves(grid: Grid) -> List[Move]:
    danger_levels = _assess_danger_levels(grid)

    least_danger_moves_list: List[Move] = list()
    least_danger_level = 1
    for point, danger_stats in danger_levels.items():
        current_danger_level, max_level = danger_stats
        danger_level = current_danger_level / max_level

        if danger_level < least_danger_level:
            least_danger_moves_list.clear()
            least_danger_level = danger_level

        if danger_level == least_danger_level:
            least_danger_moves_list.append(Move('primary', point))

    return least_danger_moves_list
