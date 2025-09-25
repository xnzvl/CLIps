from math import log10

from src.common import Action, Move, Point, SweeperConfiguration
from src.game.grids import GenericGrid, Grid
from src.game.sweeper import GameState, Result, Sweeper
from src.game.tiles import MutableTile, Tile
from src.solving.strategy import Strategy


class Bot:
    def __init__[C: SweeperConfiguration](self, sweeper: Sweeper[C], strategy: Strategy) -> None:
        self._strategy = strategy
        self._sweeper = sweeper

    def solve(self, max_attempts: int = 1, attempt_each: bool = False) -> None:
        if max_attempts < 1:
            raise ValueError("max_attempts must be a positive integer")

        victories = 0
        attempt_number = 0
        result: Result = GameState.VICTORY

        dimensions = self._sweeper.get_dimensions()
        opening_move = Move(Action.UNCOVER, Point(dimensions.width // 2, dimensions.height // 2))

        while attempt_number < max_attempts and (attempt_each or result == GameState.VICTORY):
            self._sweeper.reset()
            self._sweeper.play(opening_move)

            attempt_number += 1
            result = self._attempt_to_solve()

            if result == GameState.VICTORY:
                victories += 1
                self._sweeper.sign_victory('xnzvl')  # TODO: username shouldn't be hardcoded

            print_attempt(int(log10(max_attempts)) + 1, attempt_number, result)

        if attempt_each:
            print_winrate(victories, max_attempts)

    def _attempt_to_solve(self) -> Result:
        grid: Grid[Tile] = GenericGrid(self._sweeper.get_dimensions(), lambda: MutableTile())

        game_state: GameState = GameState.IN_PROGRESS
        while game_state == GameState.IN_PROGRESS:
            grid = self._sweeper.obtain_grid(grid)
            moves = self._strategy.apply(grid)
            i = 0

            while game_state == GameState.IN_PROGRESS and i < len(moves):
                self._sweeper.play(moves[i])

                i += 1
                game_state = self._sweeper.obtain_state()

        result = self._sweeper.obtain_state()
        assert result != GameState.IN_PROGRESS
        return result


def print_attempt(max_digits: int, attempt_number: int, result: Result) -> None:
    print(f'Attempt #{attempt_number:0{max_digits}}: {result}')


def print_winrate(victories: int, attempts: int) -> None:
    print()
    print(f'Achieved {victories} victories from {attempts} attempts')
    print(f'  => winrate: {victories / attempts * 100:.3f}%')
