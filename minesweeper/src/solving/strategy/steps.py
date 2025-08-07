from functools import reduce
from random import choice
from typing import Dict, List, Set, Tuple

from src.common import Move, Point
from src.game.grids.grid import Grid
from src.game.tiles.tile import Tile


def random_move(grid: Grid, covered_only: bool = True) -> List[Move]:
    random_moves: List[List[Move]] = list()

    for point, tile in grid:
        symbol = tile.get_symbol()

        if symbol == 'COVERED':
            random_moves.append([Move('primary', point)])
        elif not covered_only and (symbol == 'FLAG' or symbol == 'QUESTION_MARK'):
            random_moves.append([Move('secondary', point), Move('primary', point)])

    return choice(random_moves) if len(random_moves) > 0 else []


def _flag_neighbours(covered_neighbours: List[Tuple[Point, Tile]], flag_moves: List[Move], already_flagged: Set[Point]) -> None:
    for p, t in covered_neighbours:
        covered_symbol = t.get_symbol()

        if p in already_flagged or covered_symbol == 'FLAG':
            continue

        if covered_symbol == 'COVERED':
            flag_moves.append(Move('secondary', p))
        else:  # => covered_symbol == 'QUESTION_MARK'
            flag_moves.extend([Move('secondary', p)] * 2)

        already_flagged.add(p)
        t.set_sign('FLAG')


def certain_flags(grid: Grid) -> List[Move]:
    flag_moves: List[Move] = list()
    already_flagged: Set[Point] = set()

    for point, tile in grid:
        if tile.get_symbol() != 'NUMBER':
            continue

        covered_neighbours = [
            (p, t)
            for p, t in grid.get_neighbours_of_tile_at(point.x, point.y)
            if t.is_covered()
        ]
        count = tile.get_count()
        assert count is not None

        if len(covered_neighbours) != count:
            continue

        _flag_neighbours(covered_neighbours, flag_moves, already_flagged)

    return flag_moves


def certain_safe_moves(grid: Grid) -> List[Move]:
    safe_moves: List[Move] = list()

    for point, tile in grid:
        if tile.get_symbol() != 'NUMBER':
            continue

        covered_neighbours: List[Tuple[Point, Tile]] = list()
        neighbour_flags = 0

        for p, t in grid.get_neighbours_of_tile_at(point.x, point.y):
            symbol = t.get_symbol()
            if symbol == 'COVERED' or symbol == 'QUESTION_MARK':
                covered_neighbours.append((p, t))
            elif symbol == 'FLAG':
                neighbour_flags += 1

        count = tile.get_count()
        if neighbour_flags == count:
            safe_moves.extend([Move('primary', p) for p, _ in covered_neighbours])

    return safe_moves


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
