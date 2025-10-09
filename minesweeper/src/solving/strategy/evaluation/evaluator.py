from dataclasses import dataclass
from enum import Enum, auto, unique
from multiprocessing import Process, Queue
from random import randint
from time import sleep
from typing import Final, List, Tuple, assert_never

from blessed.terminal import Terminal

from src.common import Dimensions
from src.solving.strategy import Strategy


# TODO: remove magic constants in this module


ENTRIES_PER_ROW: Final = 2

RECORD_WIDTH:  Final = 42
RECORD_HEIGHT: Final = 7
RECORD_WIDTH_SPACED:  Final = RECORD_WIDTH + 4
RECORD_HEIGHT_SPACED: Final = RECORD_HEIGHT + 1

assert RECORD_HEIGHT_SPACED - RECORD_HEIGHT > 0

INDENT: Final = 2

LEADING_CHAR: Final = '.'

TERMINAL: Final = Terminal()


@unique
class FormUpdateKeyword(Enum):
    UPDATE = auto()
    DONE   = auto()


@unique
class Difficulty(Enum):
    # difficulty | mine coefficient
    EASY         = (0, 8.1)
    INTERMEDIATE = (1, 6.4)
    HARD         = (2, 4.8)


@dataclass
class FormUpdate:
    keyword: FormUpdateKeyword
    strategy_index: int
    difficulty_index: int
    value: float


class Evaluator:
    @staticmethod
    def _write(string: str) -> None:
        print(string, end='')

    @staticmethod
    def _write_md(string: str, string_length: int | None = None) -> None:
        print(
            string,
            TERMINAL.move_left(len(string) if string_length is None else string_length),
            TERMINAL.move_down(1),
            sep='', end=''
        )

    @staticmethod
    def _flush() -> None:
        print(end='', flush=True)

    @staticmethod
    def _truncate_strategy_name(strategy_name: str) -> str:
        return TERMINAL.truncate(strategy_name, RECORD_WIDTH - 13) + '...' \
            if len(strategy_name) > RECORD_WIDTH - 10 \
            else strategy_name

    @staticmethod
    def _attempts_str(attempt: int, from_attempts: int) -> str:
        just_width = RECORD_WIDTH - 4 * INDENT - 14

        txt = f' {attempt}/{from_attempts}' \
            if len(f' {from_attempts}/{from_attempts}') <= just_width \
            else ''

        return LEADING_CHAR * (just_width - len(txt)) + TERMINAL.bright_black(txt)

    @staticmethod
    def _move_to_record(record_index: int) -> None:
        row, column = record_index // ENTRIES_PER_ROW, record_index % ENTRIES_PER_ROW

        Evaluator._write(
            ('' if column == 0 else TERMINAL.move_right(column * RECORD_WIDTH_SPACED)) +
            ('' if row == 0 else TERMINAL.move_down(row * RECORD_HEIGHT_SPACED))
        )

    @staticmethod
    def _move_back_from_record(record_index: int) -> None:
        row, column = record_index // ENTRIES_PER_ROW, record_index % ENTRIES_PER_ROW

        Evaluator._write(
            ('' if column == 0 else TERMINAL.move_left(column * RECORD_WIDTH_SPACED)) +
            ('' if row == 0 else TERMINAL.move_up(row * RECORD_HEIGHT_SPACED))
        )

    def __init__(
            self,
            strategies: List[Tuple[str, Strategy]],
            dimensions: Dimensions = Dimensions(24, 24),
            testing_batch_size: int = 10
    ) -> None:
        self._strategies = strategies
        self._strategy_rows = (len(strategies) + ENTRIES_PER_ROW - 1) // ENTRIES_PER_ROW

        self._cursor_x = 0
        self._cursor_y = 0

        self.dimensions = dimensions
        self.testing_batch_size = testing_batch_size

    def _form_progress_updater(self, queue: Queue) -> None:
        update = queue.get()

        while update is not None:
            keyword = update.keyword
            strat_i, diff_i = update.strategy_index, update.difficulty_index

            Evaluator._move_to_record(strat_i)
            Evaluator._write(
                TERMINAL.move_right(18) +
                TERMINAL.move_down(4 + diff_i)
            )

            just_width = RECORD_WIDTH - 2 * INDENT - 16
            if keyword == FormUpdateKeyword.UPDATE:
                Evaluator._write(
                    Evaluator._attempts_str(int(update.value), self.testing_batch_size) +
                    TERMINAL.move_right(2)
                )
                Evaluator._flush()
            elif keyword == FormUpdateKeyword.DONE:
                Evaluator._write(f' {round(update.value, 2):.2f}%'.rjust(just_width, LEADING_CHAR), )
            else:
                assert_never(keyword)

            Evaluator._write(
                TERMINAL.move_left(RECORD_WIDTH - INDENT) +
                TERMINAL.move_up(4 + diff_i)
            )
            Evaluator._move_back_from_record(strat_i)
            Evaluator._flush()

            update = queue.get()

    def _evaluate_strategy(
            self,
            strategy_index: int,
            difficulty: Difficulty,
            queue: Queue
    ) -> None:
        width, height = self.dimensions.width, self.dimensions.height
        _, strategy = self._strategies[strategy_index]
        diff_index, diff_coefficient = difficulty.value

        # bot = BotFactory.get_minefield_bot(
        #     SweeperConfiguration(
        #         dimensions=self.dimensions,
        #         mines=int((width * height) / diff_coefficient),
        #         question_marks=False
        #     ),
        #     strategy,
        #     'evaluator',
        # )
        #
        # victories = bot.batch_solve(
        #     self.testing_batch_size,
        #     lambda i, _: queue.put(
        #         FormUpdate(
        #             keyword=FormUpdateKeyword.UPDATE,
        #             strategy_index=strategy_index,
        #             difficulty_index=diff_index,
        #             value=i
        #         )
        #     )
        # )

        t = 0
        for i in range(self.testing_batch_size):
            nap = randint(0, 500) / 100
            t += nap
            sleep(nap)
            queue.put(
                FormUpdate(
                    keyword=FormUpdateKeyword.UPDATE,
                    strategy_index=strategy_index,
                    difficulty_index=diff_index,
                    value=i + 1
                )
            )

        queue.put(
            FormUpdate(
                keyword=FormUpdateKeyword.DONE,
                strategy_index=strategy_index,
                difficulty_index=diff_index,
                value=t
            )
        )

        # winrate = victories / self.testing_batch_size

    def _evaluate_strategies(self) -> None:
        queue: Queue[FormUpdate | None] = Queue()

        form_updater = Process(
            target=self._form_progress_updater,
            args=(queue,)
        )
        form_updater.start()

        evaluators: List[Process] = list()
        for strategy_index in range(len(self._strategies)):
            for difficulty in Difficulty:
                e = Process(
                    target=self._evaluate_strategy,
                    args=(strategy_index, difficulty, queue)
                )
                e.start()
                evaluators.append(e)
        for e in evaluators:
            e.join()

        queue.put(None)
        form_updater.join()

    def _prepare_strategy_record(self, index: int) -> None:
        name, strategy = self._strategies[index]

        Evaluator._move_to_record(index)

        truncated_name = Evaluator._truncate_strategy_name(name)
        Evaluator._write_md(f'{TERMINAL.bright_white('Strategy:')} {TERMINAL.bright_blue(truncated_name)}', 10 + len(truncated_name))
        Evaluator._write_md(f'{TERMINAL.bright_white('=' * RECORD_WIDTH)}', RECORD_WIDTH)
        Evaluator._write_md(f'{INDENT * ' '}Difficulty{'Winrate'.rjust(RECORD_WIDTH - 2 * INDENT - 10, ' ')}')
        Evaluator._write_md(f'{INDENT * ' '}{'-' * (RECORD_WIDTH - INDENT * 2)}')

        for difficulty in Difficulty:
            Evaluator._write_md(
                f'{INDENT * ' '}{difficulty.name.capitalize()} {LEADING_CHAR * (15 - len(difficulty.name))}' +
                f'{Evaluator._attempts_str(0, self.testing_batch_size)}',
                RECORD_WIDTH - 2 * INDENT
            )

        Evaluator._write(TERMINAL.move_up(RECORD_HEIGHT))
        Evaluator._move_back_from_record(index)

    def _prepare_blank_page(self) -> None:
        print()
        for _ in range(self._strategy_rows):
            for _ in range(RECORD_HEIGHT_SPACED):
                print()
        Evaluator._write(
            TERMINAL.move_right(2) +
            TERMINAL.move_up(self._strategy_rows * RECORD_HEIGHT_SPACED)
        )

    def _prepare_form(self) -> None:
        self._prepare_blank_page()

        for i in range(len(self._strategies)):
            self._prepare_strategy_record(i)

        Evaluator._flush()

    def run(self) -> None:
        self._prepare_form()
        self._evaluate_strategies()
        Evaluator._write(TERMINAL.move_down(RECORD_HEIGHT_SPACED * self._strategy_rows - 1))
