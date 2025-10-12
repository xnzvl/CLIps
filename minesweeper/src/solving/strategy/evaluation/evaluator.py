from dataclasses import dataclass
from enum import Enum, unique
from functools import partial
from multiprocessing import Process, Pipe
from multiprocessing.connection import Connection
from multiprocessing.managers import SharedMemoryManager
from multiprocessing.pool import Pool
from multiprocessing.shared_memory import ShareableList
from random import randint, choice
from time import sleep
from typing import Dict, Final, List, Tuple

from blessed.terminal import Terminal

from src.common import Dimensions, SweeperConfiguration
from src.game.sweeper import Result, GameState
from src.solving.bot import BotFactory
from src.solving.strategy import Strategy
from src.solving.strategy.evaluation.throbber import Throbber
from src.utils import Repeater


# TODO: remove magic constants in this module
# TODO: separate print funcs to separate class?


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
class FormLocation:   # TODO: better name
    strategy_index: int
    difficulty_index: int


@dataclass(frozen=True)
class FormUpdate(FormLocation):   # TODO: better name
    result: Result


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
    def _submit_progress_update(
            progress_updates_sender: Connection,
            strategy_index: int,
            difficulty_index: int,
            result: Result
    ) -> None:
        progress_updates_sender.send(
            FormUpdate(
                strategy_index=strategy_index,
                difficulty_index=difficulty_index,
                result=result
            )
        )

    @staticmethod
    def _write_throbber_char(form_location: FormLocation, char: str) -> None:
        Evaluator._move_to_record_difficulty(form_location)

        horizontal_move = RECORD_WIDTH - 21
        Evaluator._write(
            TERMINAL.move_right(horizontal_move) +
            TERMINAL.blue(char)
        )

        Evaluator._move_from_record_difficulty(form_location)
        Evaluator._flush()

    @staticmethod
    def _create_active_throbber(form_location: FormLocation) -> Repeater:
        repeater = Repeater(
            0.05,
            lambda throbber: Evaluator._write_throbber_char(form_location, throbber.get_and_progress()),
            Throbber(2)
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

    def _throbber_updater(
            self,
            throbber_updates_receiver: Connection,
            throbber_ack_sender: Connection
    ) -> None:
        diff_len = len(Difficulty)

        throbbers = [
            Evaluator._create_active_throbber(
                FormLocation(
                    strategy_index=i // diff_len,
                    difficulty_index=i % diff_len,
                )
            )
            for i in range(len(self._strategies) * diff_len)
        ]

        update = throbber_updates_receiver.recv()
        while update is not None:
            throbbers[update.strategy_index * diff_len + update.difficulty_index].stop()
            sleep(0.075)
            throbber_ack_sender.send(None)

            update = throbber_updates_receiver.recv()

    def _progress_updater(
            self,
            progress_updates_receiver: Connection,
            throbber_updates_sender: Connection,
            throbber_ack_receiver: Connection,
            shared_list: ShareableList[int]
    ) -> None:
        diff_len = len(Difficulty)

        tests_completed = [ 0 for _ in range(len(self._strategies) * diff_len) ]

        update = progress_updates_receiver.recv()
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
                throbber_updates_sender.send(update)
                throbber_ack_receiver.recv()

                just_width = RECORD_WIDTH - 2 * INDENT - 16
                Evaluator._write(f' {round(shared_list[i] / self.testing_batch_size * 100, 2):.2f}%'.rjust(just_width, LEADING_CHAR), )

            Evaluator._move_from_record_difficulty(update)
            Evaluator._flush()

            update = progress_updates_receiver.recv()

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
            progress_updates_sender: Connection,
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
                        Evaluator._submit_progress_update,
                        progress_updates_sender,
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

        progress_updates_receiver, progress_updates_sender = Pipe(False)
        throbber_updates_receiver, throbber_updates_sender = Pipe(False)
        throbber_ack_receiver,     throbber_ack_sender     = Pipe(False)

        progress_updater_process = Process(
            target=self._progress_updater,
            args=(progress_updates_receiver, throbber_updates_sender, throbber_ack_receiver, shared_list)
        )
        progress_updater_process.start()

        throbber_updater_process = Process(
            target=self._throbber_updater,
            args=(throbber_updates_receiver, throbber_ack_sender)
        )
        throbber_updater_process.start()

        pool = Pool(
            processes=max_workers
        )
        for strategy_index in range(len(self._strategies)):
            self._evaluate_strategy(pool, progress_updates_sender, strategy_index)
        pool.close()
        pool.join()

        progress_updates_sender.send(None)
        progress_updater_process.join()

        throbber_updates_sender.send(None)
        throbber_updater_process.join()

        progress_updates_receiver.close()
        progress_updates_sender.close()
        throbber_updates_receiver.close()
        throbber_updates_sender.close()
        throbber_ack_receiver.close()
        throbber_ack_sender.close()

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
                f'{Evaluator._attempts_str(0, self.testing_batch_size)}' +
                f' {TERMINAL.blue('⠿')}',
                RECORD_WIDTH - INDENT
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

    def _summarize(self, evaluations: List[Tuple[str, Dict[Difficulty, float]]]) -> Tuple[Dict[Difficulty, Tuple[float, List[str]]], Tuple[float, List[str]]]:
        best_per_difficulty: Dict[Difficulty, Tuple[float, List[str]]] = dict(
            [(difficulty, (0.0, list())) for difficulty in Difficulty]
        )
        most_versatile = 0.0, list()

        for strategy_name, results in evaluations:
            continue  # TODO: implement

        return best_per_difficulty, most_versatile

    def run(self, max_workers: int = 16) -> None:
        self._prepare_form()

        summary = self._summarize(
            self._evaluate_strategies(max_workers)
        )

        Evaluator._write(TERMINAL.move_down(RECORD_HEIGHT_SPACED * self._strategy_rows - 1))


def demanding_calculation() -> Result:
    sleep(randint(1, 10) / 10)
    return choice([GameState.VICTORY, GameState.FAILURE])
