# TODO: guarantee minimal window size on Unix
# from signal import signal, SIGWINCH  # https://blessed.readthedocs.io/en/latest/measuring.html#resizing

from typing import Dict, Literal, override

from blessed.terminal import Terminal

from src.common import Dimensions
from src.game.grids.grid import Grid
from src.game.sweeper import GameState, Result
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
        self._dimensions = dimensions
        self._mines = mines

        self._term = Terminal()
        self._term.fullscreen()

        # TODO: colour these to bright_black
        self._render_header()
        self._render_grid()
        self._render_prompt()

    def _render_header(self) -> None:
        n = (3 * self._dimensions.width + self._dimensions.width + 1 - 7) // 2

        line_segment = n * HEADER_SHAPES['─']
        space_segment = n * ' '

        print(
            HEADER_SHAPES['┌'] + line_segment +
            HEADER_SHAPES['┬'] + HEADER_SHAPES['─'] * SMILEY_WIDTH + HEADER_SHAPES['┬']
                               + line_segment + HEADER_SHAPES['┐']
        )
        print(
            HEADER_SHAPES['│'] +
            space_segment +
            HEADER_SHAPES['│'] + ' ' * SMILEY_WIDTH + HEADER_SHAPES['│'] +
            space_segment +
            HEADER_SHAPES['│']
        )
        print(
            HEADER_SHAPES['└'] + line_segment +
            HEADER_SHAPES['┴'] + HEADER_SHAPES['─'] * SMILEY_WIDTH + HEADER_SHAPES['┴']
                               + line_segment + HEADER_SHAPES['┘']
        )

    def _render_grid(self) -> None:
        print(f' {GRID_SHAPES['┌']}', end='')
        for column in range(self._dimensions.width):
            print(str(column).ljust(3, GRID_SHAPES['─']), end='')

            if column < self._dimensions.width - 1:
                print(GRID_SHAPES['┬'], end='')
        print(GRID_SHAPES['┐'])

        cell_border = GRID_SHAPES['─'] * CELL_WIDTH
        for row in range(0, self._dimensions.height):
            print(f'{row:>2}' + (' ' * CELL_WIDTH + '|') * self._dimensions.width)

            if row != self._dimensions.height - 1:
                print(
                    f' {GRID_SHAPES['├']}' +
                    (cell_border + GRID_SHAPES['┼']) * (self._dimensions.width - 1) + cell_border +
                    GRID_SHAPES['┤']
                )

        print(
            f' {GRID_SHAPES['└']}' +
            (cell_border + GRID_SHAPES['┴']) * (self._dimensions.width - 1) + cell_border +
            GRID_SHAPES['┘']
        )

    def _render_prompt(self) -> None:
        print()
        print(
            self._term.bright_green('xnzvl@CLIps') +
            self._term.white(':') +
            self._term.bright_blue('/minesweeper') +
            self._term.white('$') + ' '
        )

    @override
    def render_game_state(self, game_state: GameState) -> None:
        pass

    @override
    def render_remaining_mines(self, remaining_mines: int) -> None:
        pass

    @override
    def render_grid(self, grid: Grid) -> None:
        pass

    @override
    def render_result(self, result: Result) -> None:
        pass

    @override
    def get_player_input(self, game_state: GameState) -> Input:
        # don't forget to exit fullscreen on exit
        pass
