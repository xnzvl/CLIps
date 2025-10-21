from contextlib import AbstractContextManager
from enum import Enum, auto, unique
from typing import Dict, Final, List, Tuple

from blessed import Terminal

from src.solving.strategy import Strategy

from .types import FormLocation, Difficulty, Summary, SummaryEntry


ENTRIES_PER_ROW: Final = 2

RECORD_WIDTH:  Final = 42
RECORD_HEIGHT: Final = 7
RECORD_WIDTH_SPACED:  Final = RECORD_WIDTH + 4
RECORD_HEIGHT_SPACED: Final = RECORD_HEIGHT + 1

INDENT: Final = 2
PADDING: Final = 16

LEADING_CHAR: Final = '.'


assert RECORD_WIDTH_SPACED  - RECORD_WIDTH  > 0
assert RECORD_HEIGHT_SPACED - RECORD_HEIGHT > 0
assert 2 * PADDING < RECORD_WIDTH_SPACED


TERMINAL = Terminal()


@unique
class NotePosition(Enum):
    NONE                 = auto()
    AFTER_PER_DIFFICULTY = auto()
    AT_THE_END           = auto()


class ConsoleOutput:
    def __init__(self, strategies: List[Tuple[str, Strategy]], testing_batch_size: int) -> None:
        self._strategies = strategies
        self._record_rows = (len(strategies) + ENTRIES_PER_ROW - 1) // ENTRIES_PER_ROW
        self._testing_batch_size = testing_batch_size

    def write(self, string: str) -> None:
        print(string, end='')

    def write_md(self, string: str, string_length: int | None = None) -> None:
        print(
            string,
            TERMINAL.move_left(len(string) if string_length is None else string_length),
            TERMINAL.move_down(1),
            sep='', end=''
        )

    def flush(self) -> None:
        print(end='', flush=True)

    def move_to_record(self, record_index: int) -> None:
        row, column = record_index // ENTRIES_PER_ROW, record_index % ENTRIES_PER_ROW

        self.write(
            ('' if column == 0 else TERMINAL.move_right(column * RECORD_WIDTH_SPACED)) +
            ('' if row == 0 else TERMINAL.move_down(row * RECORD_HEIGHT_SPACED))
        )

    def move_from_record(self, record_index: int) -> None:
        row, column = record_index // ENTRIES_PER_ROW, record_index % ENTRIES_PER_ROW

        self.write(
            ('' if column == 0 else TERMINAL.move_left(column * RECORD_WIDTH_SPACED)) +
            ('' if row == 0 else TERMINAL.move_up(row * RECORD_HEIGHT_SPACED))
        )

    def move_to_record_difficulty(self, form_location: FormLocation) -> None:
        self.move_to_record(form_location.strategy_index)
        self.write(
            TERMINAL.move_right(18) +
            TERMINAL.move_down(4 + form_location.difficulty_index)
        )

    def move_from_record_difficulty(self, form_location: FormLocation) -> None:
        self.write(
            TERMINAL.move_left(RECORD_WIDTH - INDENT) +
            TERMINAL.move_up(4 + form_location.difficulty_index)
        )
        self.move_from_record(form_location.strategy_index)

    def write_progress(self, tests_done: int) -> None:
        self.write(
            attempts_str(tests_done, self._testing_batch_size) +
            TERMINAL.move_right(2)
        )

    def write_winrate(self, winrate: float) -> None:
        just_width = RECORD_WIDTH - 2 * INDENT - 16
        self.write(f' {winrate:.2f}%'.rjust(just_width, LEADING_CHAR))

    def write_throbber_char(self, form_location: FormLocation, char: str) -> None:
        self.move_to_record_difficulty(form_location)

        horizontal_move = RECORD_WIDTH - 21
        self.write(
            TERMINAL.move_right(horizontal_move) +
            TERMINAL.blue(char)
        )

        self.move_from_record_difficulty(form_location)
        self.flush()

    def write_summary_per_difficulty(
            self,
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
            strategy_name = truncate_str(
                best_per_this_diff.strategy_name,
                width - 2 * INDENT - 12 - 14
            )

            print(
                f'{indent * 2}{pad}{difficulty.name.capitalize()} ' +
                f'{LEADING_CHAR * (width - 2 * INDENT - len(difficulty.name) - len(strategy_name) - 11)} ' +
                f'{strategy_name}{' ' if best_per_this_diff.is_alone_at_top else TERMINAL.bright_black('*')} ' +
                f'{best_per_this_diff.winrate:.2f}'.rjust(6) + '%'
            )

    def write_summary_overall_best(
            self,
            indent: str,
            pad: str,
            width: int,
            best_overall: SummaryEntry
    ) -> None:
        name_width = width - 27
        best_strategy_name = truncate_str(
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

    def write_summary_note(self, indent: str) -> None:
        print(TERMINAL.bright_black, end='')
        print(f'{indent}* multiple strategies')
        print(f'{indent}  achieved the same winrate,')
        print(f'{indent}  but only the first one is listed')
        print(TERMINAL.normal, end='')

    def write_summary(self, summary: Summary) -> None:  # TODO: refactor
        indent = ' ' * INDENT
        pad = ' ' * PADDING
        width = RECORD_WIDTH_SPACED + RECORD_WIDTH - 2 * PADDING

        note_position = get_note_position(summary)
        note_indent = pad + indent + ' ' * (2 * INDENT)

        print('\n\n')
        self.write_summary_per_difficulty(indent, pad, width, summary.best_per_difficulty)

        if note_position == NotePosition.AFTER_PER_DIFFICULTY:
            print()
            self.write_summary_note(note_indent)
        print('\n')

        self.write_summary_overall_best(indent, pad, width, summary.best_overall)

        if note_position == NotePosition.AT_THE_END:
            print()
            self.write_summary_note(note_indent)
        print('\n')

    def prepare_strategy_record(self, strategy_name: str, index: int) -> None:
        self.move_to_record(index)

        truncated_name = truncate_str(strategy_name, RECORD_WIDTH - 10)
        self.write_md(f'{TERMINAL.bright_white('Strategy:')} {TERMINAL.bright_blue(truncated_name)}', 10 + len(truncated_name))
        self.write_md(f'{TERMINAL.bright_white('=' * RECORD_WIDTH)}', RECORD_WIDTH)
        self.write_md(f'{INDENT * ' '}Difficulty{'Winrate'.rjust(RECORD_WIDTH - 2 * INDENT - 10, ' ')}')
        self.write_md(f'{INDENT * ' '}{'-' * (RECORD_WIDTH - INDENT * 2)}')

        for difficulty in Difficulty:
            self.write_md(
                f'{INDENT * ' '}{difficulty.name.capitalize()} {LEADING_CHAR * (15 - len(difficulty.name))}' +
                f'{attempts_str(0, self._testing_batch_size)}' +
                f' {TERMINAL.blue('⠿')}',
                RECORD_WIDTH - INDENT
            )

        self.write(TERMINAL.move_up(RECORD_HEIGHT))
        self.move_from_record(index)

    def prepare_blank_page(self) -> None:
        print()

        for _ in range(self._record_rows * RECORD_HEIGHT_SPACED - 1):
            print()

        self.write(
            TERMINAL.move_right(2) +
            TERMINAL.move_up(self._record_rows * RECORD_HEIGHT_SPACED - 1)
        )

    def prepare_evaluation_records(self) -> None:
        self.prepare_blank_page()

        for i in range(len(self._strategies)):
            strategy_name, _ = self._strategies[i]
            self.prepare_strategy_record(strategy_name, i)

        self.flush()

    def move_to_records_end(self) -> None:
        self.write(TERMINAL.move_down(RECORD_HEIGHT_SPACED * self._record_rows - 1))

    def hidden_cursor(self) -> AbstractContextManager[None, bool | None]:
        return TERMINAL.hidden_cursor()


def attempts_str(attempt: int, from_attempts: int) -> str:  # TODO: better func name
    just_width = RECORD_WIDTH - 4 * INDENT - 14

    txt = f' {attempt}/{from_attempts}' \
        if len(f' {from_attempts}/{from_attempts}') <= just_width \
        else ''

    return LEADING_CHAR * (just_width - len(txt)) + TERMINAL.bright_black(txt)


def truncate_str(strategy_name: str, max_length: int) -> str:
    return TERMINAL.truncate(strategy_name, max_length - 3) + '...' \
        if len(strategy_name) > max_length \
        else strategy_name


def get_note_position(summary: Summary) -> NotePosition:
    if not summary.best_overall.is_alone_at_top:
        return NotePosition.AT_THE_END

    for entry in summary.best_per_difficulty.values():
        if not entry.is_alone_at_top:
            return NotePosition.AFTER_PER_DIFFICULTY

    return NotePosition.NONE
