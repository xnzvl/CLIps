from typing import Callable

from src.common import Action, Move, Point, SweeperConfiguration
from src.game.grids import GenericGrid, Grid
from src.game.sweeper import GameState, Result, Sweeper
from src.game.tiles import MutableTile, Tile
from src.solving.strategy import Strategy


class Bot:
    def __init__[C: SweeperConfiguration](self, sweeper: Sweeper[C], strategy: Strategy, username: str) -> None:
        self._strategy = strategy
        self._sweeper = sweeper
        self._username = username

    def solve(self) -> Result:
        dimensions = self._sweeper.get_dimensions()

        self._sweeper.reset()
        self._sweeper.play(
            Move(Action.UNCOVER, Point(dimensions.width // 2, dimensions.height // 2))
        )

        grid: Grid[Tile] = GenericGrid(self._sweeper.get_dimensions(), MutableTile)
        game_state: GameState = GameState.IN_PROGRESS

        while game_state == GameState.IN_PROGRESS:
            grid = self._sweeper.obtain_grid(grid)
            moves = self._strategy.apply(grid)
            i = 0

            while game_state == GameState.IN_PROGRESS and i < len(moves):
                self._sweeper.play(moves[i])

                i += 1
                game_state = self._sweeper.obtain_state()

        return game_state

    def batch_solve(self, count: int, result_consumer: Callable[[int, Result], None] | None = None) -> int:
        if count < 1:
            raise ValueError('\'count\' must be a positive integer')

        victories = 0

        for i in range(count):
            result = self.solve()

            if result_consumer is not None:
                result_consumer(i, result)

            if result == GameState.VICTORY:
                victories += 1

        return victories
