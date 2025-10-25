from typing import List, override

from src.common import Move
from src.game.grids import Grid
from src.game.tiles import Tile

from ..strategy import Strategy
from ..strategy_error import StrategyError


class CompositeStrategy(Strategy):
    def __init__(self, steps: List[Strategy]) -> None:
        self._steps = steps

    @override
    def apply[T: Tile](self, grid: Grid[T]) -> List[Move]:
        for step in self._steps:
            step_moves = step.apply(grid)

            if len(step_moves) > 0:
                return step_moves

        raise StrategyError('strategy didn\'t come up with any moves')
