from typing import List

from src.common import Move
from src.game.board import Board
from src.strategy.steps import random_move
from src.strategy.strategy import Strategy


class RandomStrategy(Strategy):
    def get_moves(self, board: Board) -> List[Move]:
        return random_move(board)
