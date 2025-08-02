from math import log10
from typing import Callable

from src.common import Configuration, Move, Point
from src.game.board import Board
from src.game.literals import Result, GameState
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

        self._dimensions = configuration.dimensions
        self._board = Board(self._dimensions.width, self._dimensions.height)

    def solve(self, max_attempts = 1, attempt_each = False) -> None:
        if max_attempts < 1:
            raise ValueError("max_attempts must be a positive integer")

        victories = 0
        attempt_number = 0
        result: Result = 'failure'

        opening_move = Move('primary', Point(self._dimensions.width // 2, self._dimensions.height // 2))

        while attempt_number < max_attempts and (attempt_each or result != 'victory'):
            self._mediator.reset()
            self._mediator.play(opening_move)

            attempt_number += 1
            result = self._attempt_to_solve()

            if result == 'victory':
                victories += 1

            print_attempt(int(log10(max_attempts)) + 1, attempt_number, result)
            self._mediator.post_game_procedure()

        if attempt_each:
            print_winrate(victories, max_attempts)

    def _attempt_to_solve(self) -> Result:
        board = Board(self._dimensions.width, self._dimensions.height)

        game_state: GameState = 'inProgress'
        while game_state == 'inProgress':
            board = self._mediator.observe_board(board)
            moves = self._strategy.get_moves(board)
            i = 0

            while game_state == 'inProgress' and i < len(moves):
                self._mediator.play(moves[i])

                i += 1
                game_state = self._mediator.observe_state()

        result = self._mediator.observe_state()
        assert result != 'inProgress'
        return result


def print_attempt(max_digits: int, attempt_number: int, result: Result) -> None:
    print(f'Attempt #{attempt_number:0{max_digits}}: {result}')


def print_winrate(victories: int, attempts: int) -> None:
    print()
    print(f'Achieved {victories} victories from {attempts} attempts')
    print(f'  => winrate: {victories / attempts * 100:.3f}%')
