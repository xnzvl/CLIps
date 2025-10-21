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


# TODO: this module name
# TODO: reorder functions (group move_* and write_*)
# TODO: go over func names and make them more self-explanatory


def write(string: str) -> None:
    print(string, end='')


def write_md(string: str, string_length: int | None = None) -> None:
    print(
        string,
        TERMINAL.move_left(len(string) if string_length is None else string_length),
        TERMINAL.move_down(1),
        sep='', end=''
    )


def flush() -> None:
    print(end='', flush=True)


def truncate_str(strategy_name: str, max_length: int) -> str:
    return TERMINAL.truncate(strategy_name, max_length - 3) + '...' \
        if len(strategy_name) > max_length \
        else strategy_name


def attempts_str(attempt: int, from_attempts: int) -> str:  # TODO: better func name
    just_width = RECORD_WIDTH - 4 * INDENT - 14

    txt = f' {attempt}/{from_attempts}' \
        if len(f' {from_attempts}/{from_attempts}') <= just_width \
        else ''

    return LEADING_CHAR * (just_width - len(txt)) + TERMINAL.bright_black(txt)


def move_to_record(record_index: int) -> None:
    row, column = record_index // ENTRIES_PER_ROW, record_index % ENTRIES_PER_ROW

    write(
        ('' if column == 0 else TERMINAL.move_right(column * RECORD_WIDTH_SPACED)) +
        ('' if row == 0 else TERMINAL.move_down(row * RECORD_HEIGHT_SPACED))
    )


def move_from_record(record_index: int) -> None:
    row, column = record_index // ENTRIES_PER_ROW, record_index % ENTRIES_PER_ROW

    write(
        ('' if column == 0 else TERMINAL.move_left(column * RECORD_WIDTH_SPACED)) +
        ('' if row == 0 else TERMINAL.move_up(row * RECORD_HEIGHT_SPACED))
    )


def move_to_record_difficulty(form_location: FormLocation) -> None:
    move_to_record(form_location.strategy_index)
    write(
        TERMINAL.move_right(18) +
        TERMINAL.move_down(4 + form_location.difficulty_index)
    )


def move_from_record_difficulty(form_location: FormLocation) -> None:
    write(
        TERMINAL.move_left(RECORD_WIDTH - INDENT) +
        TERMINAL.move_up(4 + form_location.difficulty_index)
    )
    move_from_record(form_location.strategy_index)


def update_progress(tests_done: int, testing_batch_size: int) -> None:
    write(
        attempts_str(tests_done, testing_batch_size) +
        TERMINAL.move_right(2)
    )


def update_progress_done(winrate: float) -> None:
    just_width = RECORD_WIDTH - 2 * INDENT - 16
    write(f' {winrate:.2f}%'.rjust(just_width, LEADING_CHAR))


def write_throbber_char(form_location: FormLocation, char: str) -> None:
    move_to_record_difficulty(form_location)

    horizontal_move = RECORD_WIDTH - 21
    write(
        TERMINAL.move_right(horizontal_move) +
        TERMINAL.blue(char)
    )

    move_from_record_difficulty(form_location)
    flush()


def get_note_position(summary: Summary) -> NotePosition:
    if not summary.best_overall.is_alone_at_top:
        return NotePosition.AT_THE_END

    for entry in summary.best_per_difficulty.values():
        if not entry.is_alone_at_top:
            return NotePosition.AFTER_PER_DIFFICULTY

    return NotePosition.NONE


def write_summary_per_difficulty(
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


def write_summary_note(indent: str) -> None:
    print(TERMINAL.bright_black, end='')
    print(f'{indent}* multiple strategies')
    print(f'{indent}  achieved the same winrate,')
    print(f'{indent}  but only the first one is listed')
    print(TERMINAL.normal, end='')


def write_summary(summary: Summary) -> None:  # TODO: refactor
    indent = ' ' * INDENT
    pad = ' ' * PADDING
    width = RECORD_WIDTH_SPACED + RECORD_WIDTH - 2 * PADDING

    note_position = get_note_position(summary)
    note_indent = pad + indent + ' ' * (2 * INDENT)

    print('\n\n')
    write_summary_per_difficulty(indent, pad, width, summary.best_per_difficulty)

    if note_position == NotePosition.AFTER_PER_DIFFICULTY:
        print()
        write_summary_note(note_indent)
    print('\n')

    write_summary_overall_best(indent, pad, width, summary.best_overall)

    if note_position == NotePosition.AT_THE_END:
        print()
        write_summary_note(note_indent)
    print('\n')


def prepare_strategy_record(strategy_name: str, index: int, testing_batch_size: int) -> None:
    move_to_record(index)

    truncated_name = truncate_str(strategy_name, RECORD_WIDTH - 10)
    write_md(f'{TERMINAL.bright_white('Strategy:')} {TERMINAL.bright_blue(truncated_name)}', 10 + len(truncated_name))
    write_md(f'{TERMINAL.bright_white('=' * RECORD_WIDTH)}', RECORD_WIDTH)
    write_md(f'{INDENT * ' '}Difficulty{'Winrate'.rjust(RECORD_WIDTH - 2 * INDENT - 10, ' ')}')
    write_md(f'{INDENT * ' '}{'-' * (RECORD_WIDTH - INDENT * 2)}')

    for difficulty in Difficulty:
        write_md(
            f'{INDENT * ' '}{difficulty.name.capitalize()} {LEADING_CHAR * (15 - len(difficulty.name))}' +
            f'{attempts_str(0, testing_batch_size)}' +
            f' {TERMINAL.blue('⠿')}',
            RECORD_WIDTH - INDENT
        )

    write(TERMINAL.move_up(RECORD_HEIGHT))
    move_from_record(index)


def compute_record_rows(strategies: List[Tuple[str, Strategy]]) -> int:
    return (len(strategies) + ENTRIES_PER_ROW - 1) // ENTRIES_PER_ROW


def prepare_blank_page(record_rows: int) -> None:
    print()

    for _ in range(record_rows * RECORD_HEIGHT_SPACED - 1):
        print()

    write(
        TERMINAL.move_right(2) +
        TERMINAL.move_up(record_rows * RECORD_HEIGHT_SPACED - 1)
    )


def move_to_records_end(strategies: List[Tuple[str, Strategy]]) -> None:
    write(TERMINAL.move_down(RECORD_HEIGHT_SPACED * compute_record_rows(strategies) - 1))


def prepare_evaluation_records(
        strategies: List[Tuple[str, Strategy]],
        testing_batch_size: int
) -> None:
    prepare_blank_page(compute_record_rows(strategies))

    for i in range(len(strategies)):
        strategy_name, _ = strategies[i]
        prepare_strategy_record(strategy_name, i, testing_batch_size)

    flush()


def hidden_cursor() -> AbstractContextManager[None, bool | None]:
    return TERMINAL.hidden_cursor()
