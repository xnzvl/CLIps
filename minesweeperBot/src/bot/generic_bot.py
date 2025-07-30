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
            attempt_number += 1
            result = self._attempt_to_solve()

            if result == 'victory':
                victories += 1

            log_attempt(attempt_number, result)
            self._mediator.reset()
            self._mediator.post_game_procedure()

        if attempt_each:
            log_attempt(attempt_number, result)

    def _attempt_to_solve(self) -> Result:
        board = self._mediator.observe_board()

        while self._mediator.observe_state() == 'inProgress':
            i = 0
            moves = self._strategy.get_moves(board)

            while self._mediator.observe_state() == 'inProgress' and i < len(moves):
                self._mediator.play(moves[i])
                i += 1

            board = self._mediator.observe_board(board)

        result = self._mediator.observe_state()
        assert result != 'inProgress'
        return result


def log_attempt(attempt_number: int, result: Result) -> None:
    print(f'Attempt #{attempt_number}: {result}')


def log_winrate(victories: int, attempts: int) -> None:
    print()
    print(f'Achieved {victories} victories from {attempts} attempts')
    print(f'  => winrate: {victories / attempts * 100:.3f}%')
