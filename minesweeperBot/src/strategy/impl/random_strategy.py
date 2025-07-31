from random import choice
from typing import List, Tuple

from src.common import Move, Point
from src.game.board import Board
from src.game.tile import Tile
from src.strategy.strategy import Strategy


class RandomStrategy(Strategy):
    def get_moves(self, board: Board) -> List[Move]:
        available_moves: List[Tuple[Point, Tile]] = list()

        for point, tile in board:
            if tile.is_covered():
                available_moves.append((point, tile))

        chosen_point, chosen_tile = choice(available_moves)

        return [Move('primary', chosen_point)] \
            if chosen_tile.get_symbol() != 'FLAG' \
            else [
                Move('secondary', chosen_point),
                Move('primary', chosen_point),
            ]
