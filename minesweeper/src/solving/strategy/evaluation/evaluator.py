from dataclasses import dataclass
from enum import Enum, unique, auto
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
# TODO: refactor the whole module
# TODO: fix bug - overall winrate is wrong
# TODO: hide cursor


ENTRIES_PER_ROW: Final = 2

RECORD_WIDTH:  Final = 42
RECORD_HEIGHT: Final = 7
RECORD_WIDTH_SPACED:  Final = RECORD_WIDTH + 4
RECORD_HEIGHT_SPACED: Final = RECORD_HEIGHT + 1

INDENT: Final = 2
PADDING: Final = 16

LEADING_CHAR: Final = '.'

TERMINAL: Final = Terminal()

assert RECORD_WIDTH_SPACED  - RECORD_WIDTH  > 0
assert RECORD_HEIGHT_SPACED - RECORD_HEIGHT > 0
assert 2 * PADDING < RECORD_WIDTH_SPACED


@unique
class Difficulty(Enum):
    # difficulty | mine coefficient
    EASY         = (0, 8.1)
    INTERMEDIATE = (1, 6.4)
    HARD         = (2, 4.8)


@unique
class NotePosition(Enum):
    NONE                 = auto()
    AFTER_PER_DIFFICULTY = auto()
    AT_THE_END           = auto()


@dataclass(frozen=True)
class Evaluation:
    strategy_name: str
    winrate_per_difficulty: Dict[Difficulty, float]


@dataclass(frozen=True)
class FormLocation:   # TODO: better name
    strategy_index: int
    difficulty_index: int


@dataclass(frozen=True)
class FormUpdate(FormLocation):   # TODO: better name
    result: Result


@dataclass(frozen=True)
class SummaryEntry:
    strategy_name: str
    winrate: float
    is_alone_at_top: bool


@dataclass(frozen=True)
class Summary:
    best_per_difficulty: Dict[Difficulty, SummaryEntry]
    best_overall: SummaryEntry


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
    def _truncate_str(strategy_name: str, max_length: int) -> str:
        return TERMINAL.truncate(strategy_name, max_length - 3) + '...' \
            if len(strategy_name) > max_length \
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

    @staticmethod
    def _get_note_position(summary: Summary) -> NotePosition:
        if not summary.best_overall.is_alone_at_top:
            return NotePosition.AT_THE_END

        for entry in summary.best_per_difficulty.values():
            if not entry.is_alone_at_top:
                return NotePosition.AFTER_PER_DIFFICULTY

        return NotePosition.NONE

    @staticmethod
    def _write_summary_per_difficulty(
            indent: str,
            pad: str,
            width: int,
            best_per_difficulty: Dict[Difficulty, SummaryEntry]
    ) -> None:
        print(f'{indent}{pad}{TERMINAL.bright_white('Best strategy per difficulty:')}')
        print(f'{indent}{pad}{TERMINAL.bright_white('=' * width)}')
        print(f'{indent * 2}{pad}Difficulty{' ' * (width - 2 * INDENT - 27)}Strategy  Winrate')
        print(f'{indent * 2}{pad}{'-' * (width - 2 * INDENT)}')

        for difficulty in Difficulty:
            best_per_this_diff = best_per_difficulty[difficulty]
            strategy_name = Evaluator._truncate_str(
                best_per_this_diff.strategy_name,
                width - 2 * INDENT - 12 - 14
            )

            print(
                f'{indent * 2}{pad}{difficulty.name.capitalize()} ' +
                f'{LEADING_CHAR * (width - 2 * INDENT - len(difficulty.name) - len(strategy_name) - 11)} ' +
                f'{strategy_name}{' ' if best_per_this_diff.is_alone_at_top else TERMINAL.bright_black('*')} ' +
                f'{best_per_this_diff.winrate:.2f}'.rjust(6) + '%'
            )

    @staticmethod
    def _write_summary_overall_best(
            indent: str,
            pad: str,
            width: int,
            best_overall: SummaryEntry
    ) -> None:
        name_width = width - 27
        best_strategy_name = Evaluator._truncate_str(
            best_overall.strategy_name,
            name_width
        ).rjust(name_width)

        print(
            f'{indent}{pad}{TERMINAL.bright_white('Most versatile strategy:   ')}' +
            f'{TERMINAL.bright_blue(best_strategy_name)}' +
            f'{'' if best_overall.is_alone_at_top else TERMINAL.bright_black('*')}'
        )
        print(
            f'{indent}{pad}{TERMINAL.bright_white('Overall winrate:')} {' ' * (width - 24)}' +
            TERMINAL.bright_blue(f'{best_overall.winrate:.2f}%'.rjust(7))
        )
        print(f'{indent}{pad}{TERMINAL.bright_white('=' * width)}')

    @staticmethod
    def _write_summary_note(indent: str) -> None:
        print(TERMINAL.bright_black, end='')
        print(f'{indent}* multiple strategies')
        print(f'{indent}  achieved the same winrate,')
        print(f'{indent}  but only the first one is listed')
        print(TERMINAL.normal, end='')

    @staticmethod
    def _write_summary(summary: Summary) -> None:  # TODO: refactor
        indent = ' ' * INDENT
        pad = ' ' * PADDING
        width = RECORD_WIDTH_SPACED + RECORD_WIDTH - 2 * PADDING

        note_position = Evaluator._get_note_position(summary)
        note_indent = pad + indent + ' ' * (2 * INDENT)

        print('\n\n')
        Evaluator._write_summary_per_difficulty(indent, pad, width, summary.best_per_difficulty)

        if note_position == NotePosition.AFTER_PER_DIFFICULTY:
            print()
            Evaluator._write_summary_note(note_indent)
        print('\n')

        Evaluator._write_summary_overall_best(indent, pad, width, summary.best_overall)

        if note_position == NotePosition.AT_THE_END:
            print()
            Evaluator._write_summary_note(note_indent)
        print('\n')

    def __init__(
            self,
            strategies: List[Tuple[str, Strategy]],
            dimensions: Dimensions = Dimensions(24, 24),
            testing_batch_size: int = 10
    ) -> None:
        self._strategies = strategies
        self._strategy_rows = (len(strategies) + ENTRIES_PER_ROW - 1) // ENTRIES_PER_ROW

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

    def _progress_updater(  # TODO: refactor
            self,
            progress_updates_receiver: Connection,
            throbber_updates_sender: Connection,
            throbber_ack_receiver: Connection,
            victories: ShareableList[int]
    ) -> None:
        diff_len = len(Difficulty)

        tests_completed = [ 0 for _ in range(len(self._strategies) * diff_len) ]

        update = progress_updates_receiver.recv()
        while update is not None:
            Evaluator._move_to_record_difficulty(update)

            i = update.strategy_index * diff_len + update.difficulty_index

            if update.result == GameState.VICTORY:
                victories[i] += 1

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
                Evaluator._write(f' {round(victories[i] / self.testing_batch_size * 100, 2):.2f}%'.rjust(just_width, LEADING_CHAR), )

            Evaluator._move_from_record_difficulty(update)
            Evaluator._flush()

            update = progress_updates_receiver.recv()

    def _to_evaluations(self, victories: ShareableList[int]) -> List[Evaluation]:
        evaluations: List[Evaluation] = list()
        diff_len = len(Difficulty)

        for strategy_index, (strategy_name, _) in enumerate(self._strategies):
            per_difficulty: Dict[Difficulty, float] = dict()

            for difficulty_index, difficulty in enumerate(Difficulty):
                per_difficulty[difficulty] = victories[strategy_index * diff_len + difficulty_index] / self.testing_batch_size * 100

            evaluations.append(
                Evaluation(
                    strategy_name=strategy_name,
                    winrate_per_difficulty=per_difficulty
                )
            )

        return evaluations

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

    def _evaluate_strategies(self, max_workers: int) -> List[Evaluation]:  # TODO: refactor
        smm = SharedMemoryManager()
        smm.start()

        victories = smm.ShareableList(
            [0 for _ in range(len(self._strategies) * len(Difficulty))]
        )

        progress_updates_receiver, progress_updates_sender = Pipe(False)
        throbber_updates_receiver, throbber_updates_sender = Pipe(False)
        throbber_ack_receiver,     throbber_ack_sender     = Pipe(False)

        progress_updater_process = Process(
            target=self._progress_updater,
            args=(progress_updates_receiver, throbber_updates_sender, throbber_ack_receiver, victories)
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

        evaluations = self._to_evaluations(victories)

        smm.shutdown()
        smm.join()

        return evaluations

    def _prepare_strategy_record(self, index: int) -> None:
        name, strategy = self._strategies[index]

        Evaluator._move_to_record(index)

        truncated_name = Evaluator._truncate_str(name, RECORD_WIDTH - 10)
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
        for _ in range(self._strategy_rows * RECORD_HEIGHT_SPACED - 1):
            print()
        Evaluator._write(
            TERMINAL.move_right(2) +
            TERMINAL.move_up(self._strategy_rows * RECORD_HEIGHT_SPACED - 1)
        )

    def _prepare_form(self) -> None:
        self._prepare_blank_page()

        for i in range(len(self._strategies)):
            self._prepare_strategy_record(i)

        Evaluator._flush()

    def _summarise(self, evaluations: List[Evaluation]) -> Summary:  # TODO: refactor
        best_per_difficulty: Dict[Difficulty, SummaryEntry] = dict()
        best_overall: SummaryEntry | None = None

        for evaluation in evaluations:
            winrate_sum = 0

            for difficulty, winrate in evaluation.winrate_per_difficulty.items():
                best_so_far = best_per_difficulty.get(difficulty)

                if best_so_far is None or best_so_far.winrate < winrate:
                    best_per_difficulty[difficulty] = SummaryEntry(
                        strategy_name=evaluation.strategy_name,
                        winrate=winrate,
                        is_alone_at_top=True
                    )
                elif best_so_far.winrate == winrate:
                    best_per_difficulty[difficulty] = SummaryEntry(
                        strategy_name=best_so_far.strategy_name,
                        winrate=best_so_far.winrate,
                        is_alone_at_top=False
                    )

                winrate_sum += winrate

            winrate_overall = winrate_sum / 3

            if best_overall is None or best_overall.winrate < winrate_overall:
                best_overall = SummaryEntry(
                    strategy_name=evaluation.strategy_name,
                    winrate=winrate_overall,
                    is_alone_at_top=True
                )
            elif best_overall.winrate == winrate_overall:
                best_overall = SummaryEntry(
                    strategy_name=best_overall.strategy_name,
                    winrate=best_overall.winrate,
                    is_alone_at_top=False
                )

        return Summary(
            best_per_difficulty=best_per_difficulty,
            best_overall=best_overall
        )

    def run(self, max_workers: int = 16) -> None:
        self._prepare_form()

        summary = self._summarise(
            self._evaluate_strategies(max_workers)
        )
        Evaluator._write(TERMINAL.move_down(RECORD_HEIGHT_SPACED * self._strategy_rows - 1))

        Evaluator._write_summary(summary)


def demanding_calculation() -> Result:
    sleep(randint(1, 10) / 10)
    return choice([GameState.VICTORY, GameState.FAILURE])
