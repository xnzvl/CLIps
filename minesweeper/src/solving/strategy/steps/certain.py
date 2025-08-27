from typing import List, Set, Tuple

from src.common import Move, Point
from src.game.grids.grid import Grid
from src.game.tiles.tile import Tile


def _flag_neighbours(covered_neighbours: List[Tuple[Point, Tile]], flag_moves: List[Move], already_flagged: Set[Point]) -> None:
    for p, t in covered_neighbours:
        covered_symbol = t.get_symbol()

        if p in already_flagged or covered_symbol == 'FLAG':
            continue

        flag_moves.append(Move('FLAG', p))

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
            for p, t in grid.neighbourhood_of(point.x, point.y)
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

        for p, t in grid.neighbourhood_of(point.x, point.y):
            symbol = t.get_symbol()
            if symbol == 'COVERED' or symbol == 'QUESTION_MARK':
                covered_neighbours.append((p, t))
            elif symbol == 'FLAG':
                neighbour_flags += 1

        count = tile.get_count()
        if neighbour_flags == count:
            safe_moves.extend([Move('UNCOVER', p) for p, _ in covered_neighbours])

    return safe_moves


# TODO: implement fix_certain_wrong_flags() or smth like that
