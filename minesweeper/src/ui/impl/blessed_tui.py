# TODO: guarantee minimal window size on Unix
# from signal import signal, SIGWINCH  # https://blessed.readthedocs.io/en/latest/measuring.html#resizing

from typing import Dict, Literal, override

from blessed.terminal import Terminal

from src.common import Dimensions
from src.game.grids.grid import Grid
from src.game.sweeper.sweeper import GameState, Result
from src.ui.input import Input
from src.ui.ui import UI


Shape = Literal['─', '│', '┐', '┘', '└', '┌', '┼', '┬', '┤', '┴', '├']


CELL_WIDTH = 3
SMILEY_WIDTH = 5
INFO_WIDTH = 5

HEADER_SHAPES: Dict[Shape, str] = {
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

GRID_SHAPES: Dict[Shape, str] = {
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

SMILEY_FACE: Dict[GameState, str] = {  # values have to be exactly 3 chars long
    'IN_PROGRESS': ':-)',
    'VICTORY':     ':-D',
    'FAILURE':     ':-('
}


class BlessedTUI(UI):
    def __init__(self, dimensions: Dimensions, mines: int) -> None:
        super().__init__()

        self._dimensions = dimensions
        self._mines = mines

        self._term = Terminal()

        self._fullscreen = self._term.fullscreen()
        # self._fullscreen.__enter__()

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
                HEADER_SHAPES['┬'] + HEADER_SHAPES['─'] * SMILEY_WIDTH + HEADER_SHAPES['┬']
                                   + line_segment + HEADER_SHAPES['┐']
            )
        )
        print(
            self._as_border(HEADER_SHAPES['│']) +
            space_segment +
            self._as_border(HEADER_SHAPES['│']) + ' ' * SMILEY_WIDTH + self._as_border(HEADER_SHAPES['│']) +
            space_segment +
            self._as_border(HEADER_SHAPES['│'])
        )
        print(
            self._as_border(
                HEADER_SHAPES['└'] + line_segment +
                HEADER_SHAPES['┴'] + HEADER_SHAPES['─'] * SMILEY_WIDTH + HEADER_SHAPES['┴']
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
            self._term.bright_green('xnzvl@CLIps') +  # TODO: remove hardcoded username
            self._term.white(':') +
            self._term.bright_blue('/minesweeper') +
            self._term.white('$') + ' '
        )

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

        print(
            self._term.move_xy(self._dimensions.width * 4 - 4, 1) +
            f'{mins:>02}:{secs:>02}',
            end=''
        )

    @override
    def render_game_state(self, game_state: GameState) -> None:
        print(
            self._term.move_xy((self._dimensions.width * 4) // 2, 1) +
            SMILEY_FACE[game_state],
            end=''
        )

    @override
    def render_grid(self, grid: Grid) -> None:
        for point, tile in grid:
            print(
                self._term.move_xy(2 + point.x * 4, 4 + point.y * 2) +
                '#',
                end=''
            )

    @override
    def render_result(self, result: Result) -> None:
        pass

    @override
    def get_player_input(self, game_state: GameState) -> Input:
        # don't forget to exit fullscreen on exit
        print(
            self._term.move_xy(26, self._dimensions.height * 2 + 5),  # TODO: adapt to variable username
            end=''
        )
        input()
