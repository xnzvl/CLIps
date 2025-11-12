# TODO: guarantee minimal window size on Unix
# from signal import signal, SIGWINCH  # https://blessed.readthedocs.io/en/latest/measuring.html#resizing

from typing import Dict, Final, Literal, assert_never, override, Callable, Tuple

from blessed.terminal import Terminal

from src.common import Dimensions, Action
from src.game.grids import Grid
from src.game.sweeper import GameState, Result
from src.game.tiles import MineCount, Tile, Symbol
from src.ui import Input, UI
from src.ui.ui_error import UIError
from src.ui.utils import obtain_tui_input
from src.utils import Attempt, attempt

type Shape = Literal['─', '│', '┐', '┘', '└', '┌', '┼', '┬', '┤', '┴', '├']


CELL_WIDTH:  Final = 3
EMOJI_WIDTH: Final = 5
INFO_WIDTH:  Final = 5

HEADER_SHAPES: Final[Dict[Shape, str]] = {
    '─': '═',
    '│': '║',
    '┐': '╗',
    '┘': '╝',
    '└': '╚',
    '┌': '╔',
    '┼': '╬',
    '┬': '╦',
    '┤': '╣',
    '┴': '╩',
    '├': '╠'
}

GRID_SHAPES: Final[Dict[Shape, str]] = {
    '─': '─',
    '│': '│',
    '┐': '┐',
    '┘': '┘',
    '└': '└',
    '┌': '┌',
    '┼': '┼',
    '┬': '┬',
    '┤': '┤',
    '┴': '┴',
    '├': '├'
}

EMOJI_STR: Final[Dict[GameState, str]] = {  # values have to be exactly 3 chars long
    GameState.IN_PROGRESS: ':-)',
    GameState.VICTORY:     ':-D',
    GameState.FAILURE:     ':-('
}


class BlessedTUI(UI):
    def __init__(self, dimensions: Dimensions, username: str) -> None:
        super().__init__(dimensions, username)

        self._term = Terminal()

        self._fullscreen = self._term.fullscreen()
        # self._fullscreen.__enter__()  # TODO: isn't there a better method for that?

        print(self._term.clear, end='')

        self._render_header()
        self._render_grid()
        self._render_prompt()

    def _as_border(self, string: str) -> str:
        return self._term.bright_black(string)

    def _render_header(self) -> None:
        n = (3 * self._dimensions.width + self._dimensions.width + 1 - 7) // 2

        line_segment = n * HEADER_SHAPES['─']
        space_segment = n * ' '

        print(
            self._as_border(
                HEADER_SHAPES['┌'] + line_segment +
                HEADER_SHAPES['┬'] + HEADER_SHAPES['─'] * EMOJI_WIDTH + HEADER_SHAPES['┬']
                + line_segment + HEADER_SHAPES['┐']
            )
        )
        print(
            self._as_border(HEADER_SHAPES['│']) +
            space_segment +
            self._as_border(HEADER_SHAPES['│']) + ' ' * EMOJI_WIDTH + self._as_border(HEADER_SHAPES['│']) +
            space_segment +
            self._as_border(HEADER_SHAPES['│'])
        )
        print(
            self._as_border(
                HEADER_SHAPES['└'] + line_segment +
                HEADER_SHAPES['┴'] + HEADER_SHAPES['─'] * EMOJI_WIDTH + HEADER_SHAPES['┴']
                + line_segment + HEADER_SHAPES['┘']
            )
        )

    def _render_column_header(self) -> None:
        print(
            self._as_border(f' {GRID_SHAPES['┌']}'),
            end=''
        )

        for column in range(self._dimensions.width):
            print(
                self._as_border(str(column).ljust(3, GRID_SHAPES['─'])),
                end=''
            )

            if column < self._dimensions.width - 1:
                print(
                    self._as_border(GRID_SHAPES['┬']),
                    end=''
                )

        print(
            self._as_border(GRID_SHAPES['┐'])
        )

    def _render_grid(self) -> None:
        self._render_column_header()

        cell_border = GRID_SHAPES['─'] * CELL_WIDTH
        for row in range(0, self._dimensions.height):
            print(
                self._as_border(f'{row:>2}' + (' ' * CELL_WIDTH + GRID_SHAPES['│']) * self._dimensions.width)
            )

            if row != self._dimensions.height - 1:
                print(
                    self._as_border(
                        f' {GRID_SHAPES['├']}' +
                        (cell_border + GRID_SHAPES['┼']) * (self._dimensions.width - 1) + cell_border +
                        GRID_SHAPES['┤']
                    )
                )

        print(
            self._as_border(
                f' {GRID_SHAPES['└']}' +
                (cell_border + GRID_SHAPES['┴']) * (self._dimensions.width - 1) + cell_border +
                GRID_SHAPES['┘']
            )
        )

    def _render_prompt(self) -> None:
        print()
        print(
            self._term.bright_green(f'{self._username}@CLIps') +  # TODO: remove hardcoded username
            self._term.white(':') +
            self._term.bright_blue('/minesweeper') +
            self._term.white('$') + ' '
        )

    def _dye_number(self, number: MineCount) -> str:
        num_str = str(number)

        match number:
            case 1:
                return self._term.bright_blue(num_str)
            case 2:
                return self._term.bright_green(num_str)
            case 3:
                return self._term.bright_red(num_str)
            case 4:
                return self._term.blue(num_str)
            case 5:
                return self._term.brown(num_str)
            case 6:
                return self._term.cyan(num_str)
            case 7:
                return self._term.dimgray(num_str)
            case 8:
                return self._term.silver(num_str)

    def _tile_representation(self, tile: Tile) -> str:
        symbol = tile.get_symbol()

        match symbol:
            case Symbol.COVER:
                return '▐█▌'
            case Symbol.FLAG:
                return f'▐{self._term.reverse_on_darkred('P')}▌'
            case Symbol.QUESTION_MARK:
                return f'▐{self._term.reverse('?')}▌'
            case Symbol.EXPLODED_MINE:
                return f'{self._term.red('▐')}{self._term.black_on_red('*')}{self._term.red('▌')}'
            case Symbol.MINE:
                return f'▐{self._term.reverse('*')}▌'
            case Symbol.WRONG_FLAG:
                return f'{self._term.darkred('▐')}{self._term.black_on_darkred('P')}{self._term.darkred('▌')}'
            case Symbol.EMPTY:
                return '   '
            case Symbol.NUMBER:
                mines = tile.get_count()
                assert mines is not None

                return f' {self._dye_number(mines)} '

    def _render_error_message(self, message: str, with_help: bool) -> None:
        print(
            self._term.bright_black +
            '\n' +
            '  Invalid input:\n' +
            f'    {message}'
        )

        if with_help:
            print(
                '\n' +
                '  Try:\n' +
                '    [u |uncover ] <column> <row>\n' +
                '    [f |flag    ] <column> <row>\n' +
                '    [qm|question] <column> <row>\n' +
                '    [c |clear   ] <column> <row>\n' +
                '    [r |reset   ]\n' +
                '    [q |quit    ]'
            )

        print(self._term.normal)

    def _clear_error_message(self) -> None:
        # TODO
        pass

    def _validate_input_attempt(self, attempt: Attempt[Input, str]) -> Attempt[Input, Tuple[str, bool]]:
        if not attempt.is_successful:
            return Attempt.failure((attempt.error, True))

        provided_input = attempt.result

        if provided_input.action == Action.QUIT or provided_input.action == Action.QUIT:
            return Attempt.success(provided_input)

        input_point = provided_input.move.point
        x, y = input_point.x, input_point.y

        if x < 0 or self._dimensions.width - 1 < x:
            return Attempt.failure((f'<row> has must be from range <0, {self._dimensions.width - 1}>', False))
        if y < 0 or self._dimensions.height - 1 < y:
            return Attempt.failure((f'<column> has must be from range <0, {self._dimensions.height - 1}>', False))

        return Attempt.success(provided_input)

    @override
    def render_remaining_mines(self, remaining_mines: int) -> None:
        mines = f'{min(remaining_mines, 999):>03}' \
            if remaining_mines > 0 \
            else f'-{max(remaining_mines, -99) * (-1):>02}'

        print(
            self._term.move_xy(2, 1) +
            f'M:{mines}',
            end=''
        )

    @override
    def render_time(self, seconds: int) -> None:
        mins, secs = divmod(seconds, 60)

        if mins >= 99:
            mins = min(mins, 99)
            secs = min(seconds - 99 * 60, 99)

        with self._term.hidden_cursor(), self._term.location(self._dimensions.width * 4 - 4, 1):
            print(
                f'{mins:>02}:{secs:>02}',
                end='',
                flush=True
            )

    @override
    def render_game_state(self, game_state: GameState) -> None:
        match game_state:
            case GameState.IN_PROGRESS:
                formatter = self._term.bright_yellow
            case GameState.VICTORY:
                formatter = self._term.bright_green
            case GameState.FAILURE:
                formatter = self._term.bright_red
            case _:
                assert_never(game_state)

        print(
            self._term.move_xy((self._dimensions.width * 4) // 2, 1) +
            formatter(EMOJI_STR[game_state]),
            end=''
        )

    @override
    def render_grid[T: Tile](self, grid: Grid[T]) -> None:
        if grid.get_dimensions() != self._dimensions:
            raise UIError('dimensions do not match')

        for point, tile in grid:
            print(
                self._term.move_xy(2 + point.x * 4, 4 + point.y * 2) +
                self._tile_representation(tile),
                end=''
            )

    @override
    def render_result(self, result: Result) -> None:
        # TODO: implement
        pass

    @override
    def get_player_input(self, game_state: GameState) -> Input:
        # don't forget to exit fullscreen on exit

        while True:
            print(
                self._term.move_xy(21 + len(self._username),
                self._dimensions.height * 2 + 5) + self._term.clear_eol,  # TODO: adapt to variable username
                end='',
                sep=''
            )

            validated_input = self._validate_input_attempt(
                obtain_tui_input(game_state == GameState.IN_PROGRESS)
            )

            if validated_input.is_successful:
                return validated_input.result

            error_message, should_render_help = validated_input.error
            self._render_error_message(error_message, should_render_help)
