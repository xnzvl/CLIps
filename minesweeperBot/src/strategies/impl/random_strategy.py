from typing import List
from random import randint

from src.common import Move, Point
from src.game.board import Board
from src.strategies.strategy import Strategy


class RandomStrategy(Strategy):
    def get_moves(self, board: Board) -> List[Move]:
        return [
            Move(
                'left',
                Point(randint(0, board.get_width() - 1), randint(0, board.get_height() - 1))
            )
        ]
