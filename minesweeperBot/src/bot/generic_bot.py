from typing import Callable

from src.common import Configuration
from src.game.board import Board
from src.game.literals import Result
from src.mediator.mediator import Mediator
from src.strategy.strategy import Strategy


class GenericBot:
    def __init__(
            self,
            configuration: Configuration,
            strategy: Strategy,
            mediator_instantiator: Callable[[Configuration], Mediator]
    ) -> None:
        self._strategy = strategy
        self._mediator = mediator_instantiator(configuration)

        self._board = Board(configuration.dimensions.width, configuration.dimensions.height)

    def solve(self, max_attempts = 1, attempt_each = False) -> None:
        if max_attempts < 1:
            raise ValueError("max_attempts must be a positive integer")

        victories = 0
        attempt_number = 0
        result: Result = 'failure'

        while attempt_number < max_attempts and (attempt_each or result != 'victory'):
            self._mediator.reset()

            attempt_number += 1
            result = self._attempt_to_solve()

            if result == 'victory':
                victories += 1

            print_attempt(attempt_number, result)
            self._mediator.post_game_procedure()

        if attempt_each:
            print_winrate(victories, max_attempts)

    def _attempt_to_solve(self) -> Result:
        # TODO: perhaps create a Board from configuration?
        board = self._mediator.observe_board()

        # TODO: looping here could be better (rn it's observing state 2x in a row)
        while self._mediator.observe_state() == 'inProgress':
            board = self._mediator.observe_board(board)

            i = 0
            moves = self._strategy.get_moves(board)

            while self._mediator.observe_state() == 'inProgress' and i < len(moves):
                self._mediator.play(moves[i])
                i += 1

        result = self._mediator.observe_state()
        assert result != 'inProgress'
        return result


def print_attempt(attempt_number: int, result: Result) -> None:
    print(f'Attempt #{attempt_number}: {result}')


def print_winrate(victories: int, attempts: int) -> None:
    print()
    print(f'Achieved {victories} victories from {attempts} attempts')
    print(f'  => winrate: {victories / attempts * 100:.3f}%')
