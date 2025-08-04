from random import choice
from typing import Dict, List, Set, Tuple

from src.common import Move, Point
from src.game.grids.grid import Grid
from src.game.tiles.tile import Tile


# TODO: make compatible with question-mark tiles
def random_move(board: Grid) -> List[Move]:
    covered_tiles = [
        (point, tile)
        for point, tile in board
        if tile.get_symbol() == 'COVERED'
    ]

    chosen_point, chosen_tile = choice(covered_tiles)

    return [Move('primary', chosen_point)]


# TODO: make compatible with question-mark tiles
def certain_flags(board: Grid) -> List[Move]:
    flag_moves: List[Move] = list()
    already_flagged: Set[Point] = set()

    for point, tile in board:
        if tile.get_symbol() != 'NUMBER':
            continue

        covered_neighbours = [
            (p, t)
            for p, t in board.get_neighbours_of_tile_at(point.x, point.y)
            if t.is_covered()
        ]
        count = tile.get_count()
        assert count is not None

        if len(covered_neighbours) != count:
            continue

        for p, t in covered_neighbours:
            if p not in already_flagged and t.get_symbol() == 'COVERED':
                already_flagged.add(p)
                flag_moves.append(Move('secondary', p))
                t.set_sign('FLAG')

    return flag_moves


# TODO: make compatible with question-mark tiles
def certain_safe_moves(board: Grid) -> List[Move]:
    safe_moves: List[Move] = list()

    for point, tile in board:
        if tile.get_symbol() != 'NUMBER':
            continue

        covered_neighbours: List[Tuple[Point, Tile]] = list()
        neighbour_flags = 0

        for p, t in board.get_neighbours_of_tile_at(point.x, point.y):
            symbol = t.get_symbol()
            if symbol == 'COVERED':
                covered_neighbours.append((p, t))
            elif symbol == 'FLAG':
                neighbour_flags += 1

        count = tile.get_count()
        if neighbour_flags == count:
            safe_moves.extend([Move('primary', p) for p, _ in covered_neighbours])

    return safe_moves


# TODO: make compatible with question-mark tiles
def least_danger_moves(board: Grid) -> List[Move]:
    # TODO: code polish
    danger_levels: Dict[Point, Tuple[int, int]] = dict()
    for point, tile in board:
        if tile.get_symbol() != 'NUMBER':
            continue

        neighbours = board.get_neighbours_of_tile_at(point.x, point.y)
        flags = 0

        for neighbour_point, neighbour_tile in neighbours:
            if neighbour_tile.get_symbol() == 'FLAG':
                flags += 1

        count = tile.get_count()
        assert count is not None
        if flags > count:
            raise RuntimeError('invalid state - too many flags')

        danger_increase = 1 if flags < count else 0
        for neighbour_point, neighbour_tile in neighbours:
            if neighbour_tile.get_symbol() == 'COVERED':
                danger_level, max_danger = danger_levels.get(neighbour_point, (0, 0))
                danger_levels[neighbour_point] = (danger_level + danger_increase, max_danger + 1)

    least_danger_moves_list: List[Move] = list()
    least_danger_level = 1
    for point, levels in danger_levels.items():
        current_level, max_level = levels
        danger = current_level / max_level

        if danger < least_danger_level:
            least_danger_moves_list.clear()
            least_danger_level = danger

        if danger == least_danger_level:
            least_danger_moves_list.append(Move('primary', point))

    return least_danger_moves_list
