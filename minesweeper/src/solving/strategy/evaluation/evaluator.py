from enum import Enum
from typing import Callable, Dict, Final, List, Tuple

from blessed.terminal import Terminal

from src.common import Dimensions, SweeperConfiguration
from src.solving.bot import BotFactory
from src.solving.strategy import Strategy


RECORD_WIDTH:  Final = 42
RECORD_HEIGHT: Final = 8


class Difficulty(Enum):
    # difficulty | mine coefficient
    EASY         = 8.1
    INTERMEDIATE = 6.4
    HARD         = 4.8


class Evaluator:
    def __init__(
            self,
            strategies: List[Tuple[str, Strategy]],
            dimensions: Dimensions = Dimensions(24, 24),
            testing_batch_size: int = 1000
    ) -> None:
        self._strategies = strategies
        self._term = Terminal()

        self._cursor_x = 0
        self._cursor_y = 0

        self.dimensions = dimensions
        self.testing_batch_size = testing_batch_size

    def _print(self, string: str) -> None:
        print(
            string,
            self._term.move_left(len(string)),
            self._term.move_down(1),
            sep='', end=''
        )

    def _evaluate_strategy(
            self,
            strategy: Strategy,
            difficulty: Difficulty,
            observer: Callable[[int], None]
    ) -> float:
        width, height = self.dimensions.width, self.dimensions.height

        bot = BotFactory.get_minefield_bot(
            SweeperConfiguration(
                dimensions=self.dimensions,
                mines=int((width * height) / difficulty.value),
                question_marks=False
            ),
            strategy,
            'evaluator',
        )

        victories = bot.batch_solve(
            self.testing_batch_size,
            lambda i, _: observer(i)
        )

        return victories / self.testing_batch_size

    def _prepare_strategy_record(self, index: int) -> None:
        name, strategy = self._strategies[index]
        record_x, record_y = index % 2, index // 2

        print(
            self._term.move_right(record_x * RECORD_WIDTH - 1),
            '' if record_y == 0 else self._term.move_down(record_y * RECORD_HEIGHT),
            # ^^ because move_down(0) behaves like move_down(1) ^^
            sep='', end=''
        )

        self._print(f'  Strategy: {name}')
        self._print(f'  {'=' * 38}')

        self._print('    Difficulty                 Winrate')
        self._print('    ' + '-' * 34)
        for difficulty in Difficulty:
            self._print(f'    {difficulty.name.capitalize()} {'.' * (33 - len(difficulty.name))}')
        self._print('')

        print(
            self._term.move_left(record_x * RECORD_WIDTH),
            self._term.move_up((record_y + 1) * RECORD_HEIGHT),
            sep='', end=''
        )

    def _prepare_form(self) -> None:
        print()

        strategies_count = len(self._strategies)

        for i in range(strategies_count):
            self._prepare_strategy_record(i)

        print(self._term.move_down(((strategies_count + 1) // 2) * RECORD_HEIGHT - 1))

    def _evaluate_strategies(self) -> List[Tuple[str, Dict[Difficulty, float]]]:
        self._prepare_form()

        for i, (_, strategy) in enumerate(self._strategies):  # TODO: make parallel
            for difficulty in Difficulty:  # TODO: make parallel
                self._evaluate_strategy(strategy, difficulty, lambda _: None)  # TODO: create observers
                # TODO: update strategy record

        return list()

    def run(self) -> None:
        evaluations = self._evaluate_strategies()
