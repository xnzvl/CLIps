from typing import List

from src.common import Move
from src.game.board import Board
from src.strategy.steps import certain_flags, certain_safe_moves, random_move
from src.strategy.strategy import Strategy


class CertainFirstStrategy(Strategy):
    def get_moves(self, board: Board) -> List[Move]:
        certain_moves = certain_flags(board)
        certain_moves.extend(certain_safe_moves(board))

        return certain_moves \
            if len(certain_moves) > 0 \
            else random_move(board)
