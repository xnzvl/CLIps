from typing import List

from src.common import Move
from src.game.grids import Grid
from src.game.tiles import Tile
from src.solving.strategy.steps import Step

from .strategy_error import StrategyError


class Strategy:
    def __init__(self, steps: List[Step]) -> None:
        self._steps = steps

    def apply[T: Tile](self, grid: Grid[T]) -> List[Move]:
        for step in self._steps:
            step_moves = step.get_moves(grid)

            if len(step_moves) > 0:
                return step_moves

        raise StrategyError('strategy didn\'t come up with any moves')
