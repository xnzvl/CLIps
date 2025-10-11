from dataclasses import dataclass
from enum import Enum, unique
from functools import partial
from multiprocessing import Process, Queue
from multiprocessing.managers import SharedMemoryManager
from multiprocessing.queues import Queue as MpQueue
from multiprocessing.pool import Pool
from multiprocessing.shared_memory import ShareableList
from random import randint
from time import sleep
from typing import Dict, Final, List, Tuple, TYPE_CHECKING

from blessed.terminal import Terminal

from src.common import Dimensions, SweeperConfiguration
from src.game.sweeper import Result, GameState
from src.solving.bot import BotFactory
from src.solving.strategy import Strategy
from src.solving.strategy.evaluation.throbber import Throbber
from src.utils import Repeater


# TODO: remove magic constants in this module
# TODO: separate print funcs to separate class?
# TODO: use pipes instead of queues?


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
class Difficulty(Enum):
    # difficulty | mine coefficient
    EASY         = (0, 8.1)
    INTERMEDIATE = (1, 6.4)
    HARD         = (2, 4.8)


@dataclass(frozen=True)
class FormLocation:   # TODO: better name (+ queue)
    strategy_index: int
    difficulty_index: int


@dataclass(frozen=True)
class FormUpdate(FormLocation):   # TODO: better name (+ queue)
    result: Result


if TYPE_CHECKING:
    type FormLocationQueue = MpQueue[FormLocation | None]
    type FormUpdatesQueue = MpQueue[FormUpdate | None]
else:
    type FormLocationQueue = Queue
    type FormUpdatesQueue = Queue


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
    def _move_from_record(record_index: int) -> None:
        row, column = record_index // ENTRIES_PER_ROW, record_index % ENTRIES_PER_ROW

        Evaluator._write(
            ('' if column == 0 else TERMINAL.move_left(column * RECORD_WIDTH_SPACED)) +
            ('' if row == 0 else TERMINAL.move_up(row * RECORD_HEIGHT_SPACED))
        )

    @staticmethod
    def _move_to_record_difficulty(form_location: FormLocation) -> None:
        Evaluator._move_to_record(form_location.strategy_index)
        Evaluator._write(
            TERMINAL.move_right(18) +
            TERMINAL.move_down(4 + form_location.difficulty_index)
        )

    @staticmethod
    def _move_from_record_difficulty(form_location: FormLocation) -> None:
        Evaluator._write(
            TERMINAL.move_left(RECORD_WIDTH - INDENT) +
            TERMINAL.move_up(4 + form_location.difficulty_index)
        )
        Evaluator._move_from_record(form_location.strategy_index)

    @staticmethod
    def _submit_form_update(
            form_updates: FormUpdatesQueue,
            strategy_index: int,
            difficulty_index: int,
            result: Result
    ) -> None:
        form_updates.put(
            FormUpdate(
                strategy_index=strategy_index,
                difficulty_index=difficulty_index,
                result=result
            )
        )

    @staticmethod
    def _create_active_throbber(index: int) -> Repeater:
        throbber = Throbber()

        repeater = Repeater(
            1,
            lambda: None
        )

        repeater.start()
        return repeater

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

    def _throbber_updater(self, throbber_updates: FormLocationQueue) -> None:
        diff_len = len(Difficulty)

        throbbers = [
            Evaluator._create_active_throbber(i)
            for i in range(len(self._strategies) * diff_len)
        ]

        update = throbber_updates.get()
        while update is not None:
            throbbers[update.strategy_index * diff_len + update.difficulty_index].stop()

            update = throbber_updates.get()

    def _form_progress_updater(self, form_updates: FormUpdatesQueue, throbber_updates: FormLocationQueue, shared_list: ShareableList[int]) -> None:
        diff_len = len(Difficulty)

        tests_completed = [ 0 for _ in range(len(self._strategies) * diff_len) ]

        update = form_updates.get()
        while update is not None:
            Evaluator._move_to_record_difficulty(update)

            i = update.strategy_index * diff_len + update.difficulty_index

            if update.result == GameState.VICTORY:
                shared_list[i] += 1

            tests_completed[i] += 1
            tests_done = tests_completed[i]

            if tests_done != self.testing_batch_size:
                Evaluator._write(
                    Evaluator._attempts_str(tests_done, self.testing_batch_size) +
                    TERMINAL.move_right(2)
                )
            else:
                throbber_updates.put(update)
                just_width = RECORD_WIDTH - 2 * INDENT - 16
                Evaluator._write(f' {round(shared_list[i] / self.testing_batch_size * 100, 2):.2f}%'.rjust(just_width, LEADING_CHAR), )

            Evaluator._move_from_record_difficulty(update)
            Evaluator._flush()

            update = form_updates.get()

    def _summarize(self, shared_list: ShareableList[int]) -> List[Tuple[str, Dict[Difficulty, float]]]:
        summary: List[Tuple[str, Dict[Difficulty, float]]] = list()
        diff_len = len(Difficulty)

        for strategy_index, (strategy_name, _) in enumerate(self._strategies):
            per_strategy: Dict[Difficulty, float] = dict()

            for difficulty_index, difficulty in enumerate(Difficulty):
                per_strategy[difficulty] = shared_list[strategy_index * diff_len + difficulty_index] / self.testing_batch_size * 100

            summary.append((strategy_name, per_strategy))

        return summary

    def _evaluate_strategy(
            self,
            pool: Pool,
            form_updates: FormUpdatesQueue,
            strategy_index: int
    ) -> None:
        strategy_name, strategy = self._strategies[strategy_index]

        for difficulty in Difficulty:
            diff_index, diff_coefficient = difficulty.value

            bot = BotFactory.get_minefield_bot(
                SweeperConfiguration(
                    dimensions=self.dimensions,
                    mines=int((self.dimensions.width * self.dimensions.height) / diff_coefficient),
                    question_marks=False
                ),
                strategy,
                f'evaluator::{strategy_name}',
            )

            for _ in range(self.testing_batch_size):
                pool.apply_async(
                    func=demanding_calculation,  # bot.solve,  # TODO: uncomment
                    callback=partial(
                        Evaluator._submit_form_update,
                        form_updates,
                        strategy_index,
                        diff_index
                    )
                )

    def _evaluate_strategies(self, max_workers: int) -> List[Tuple[str, Dict[Difficulty, float]]]:
        smm = SharedMemoryManager()
        smm.start()

        shared_list = smm.ShareableList(
            [0 for _ in range(len(self._strategies) * len(Difficulty))]
        )
        form_updates: FormUpdatesQueue = Queue()
        throbber_updates: FormUpdatesQueue = Queue()

        form_updates_process = Process(
            target=self._form_progress_updater,
            args=(form_updates, throbber_updates, shared_list)
        )
        form_updates_process.start()

        throbber_updates_process = Process(
            target=self._throbber_updater,
            args=(throbber_updates,)
        )
        throbber_updates_process.start()

        pool = Pool(
            processes=max_workers
        )
        for strategy_index in range(len(self._strategies)):
            self._evaluate_strategy(pool, form_updates, strategy_index)
        pool.close()
        pool.join()

        throbber_updates.put(None)
        throbber_updates_process.join()

        form_updates.put(None)
        form_updates_process.join()

        summary = self._summarize(shared_list)

        smm.shutdown()
        smm.join()

        return summary

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
        Evaluator._move_from_record(index)

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

    def run(self, max_workers = 16) -> None:
        self._prepare_form()

        summary = self._evaluate_strategies(max_workers)

        Evaluator._write(TERMINAL.move_down(RECORD_HEIGHT_SPACED * self._strategy_rows - 1))


def demanding_calculation() -> Result:
    sleep(randint(1, 4))
    return GameState.VICTORY
