from random import choice
from typing import List, Set, Tuple

from src.common import Move, Point
from src.game.board import Board
from src.game.tile import Tile


def random_move(board: Board) -> List[Move]:
    covered_tiles = [
        (point, tile)
        for point, tile in board
        if tile.get_symbol() == 'COVERED'
    ]

    chosen_point, chosen_tile = choice(covered_tiles)

    return [Move('primary', chosen_point)]


# TODO: make compatible with question-mark tiles
def certain_flags(board: Board) -> List[Move]:
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


def certain_safe_moves(board: Board) -> List[Move]:
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
