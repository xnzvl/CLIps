from math import log10
from typing import Callable

from src.common import Configuration, Move, Point
from src.game.grids.impl.generic_grid import GenericGrid
from src.game.literals import GameState, Result
from src.mediator.mediator import Mediator
from src.solving.strategy.strategy import Strategy


class GenericBot:
    def __init__(
            self,
            configuration: Configuration,
            strategy: Strategy,
            mediator_instantiator: Callable[[Configuration], Mediator]
    ) -> None:
        self._strategy = strategy
        self._mediator = mediator_instantiator(configuration)

        self._dimensions = configuration.dimensions
        self._grid = GenericGrid(self._dimensions)

    def solve(self, max_attempts = 1, attempt_each = False) -> None:
        if max_attempts < 1:
            raise ValueError("max_attempts must be a positive integer")

        victories = 0
        attempt_number = 0
        result: Result = 'VICTORY'

        opening_move = Move('UNCOVER', Point(self._dimensions.width // 2, self._dimensions.height // 2))

        while attempt_number < max_attempts and (attempt_each or result == 'VICTORY'):
            self._mediator.reset()
            self._mediator.play(opening_move)

            attempt_number += 1
            result = self._attempt_to_solve()

            if result == 'VICTORY':
                victories += 1

            print_attempt(int(log10(max_attempts)) + 1, attempt_number, result)
            self._mediator.post_game_procedure()

        if attempt_each:
            print_winrate(victories, max_attempts)

    def _attempt_to_solve(self) -> Result:
        grid = GenericGrid(self._dimensions)

        game_state: GameState = 'IN_PROGRESS'
        while game_state == 'IN_PROGRESS':
            grid = self._mediator.observe_grid(grid)
            moves = self._strategy.get_moves(grid)
            i = 0

            while game_state == 'IN_PROGRESS' and i < len(moves):
                self._mediator.play(moves[i])

                i += 1
                game_state = self._mediator.observe_state()

        result = self._mediator.observe_state()
        assert result != 'IN_PROGRESS'
        return result


def print_attempt(max_digits: int, attempt_number: int, result: Result) -> None:
    print(f'Attempt #{attempt_number:0{max_digits}}: {result}')


def print_winrate(victories: int, attempts: int) -> None:
    print()
    print(f'Achieved {victories} victories from {attempts} attempts')
    print(f'  => winrate: {victories / attempts * 100:.3f}%')
