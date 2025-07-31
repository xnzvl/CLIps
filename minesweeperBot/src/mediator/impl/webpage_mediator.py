from typing import Dict, Tuple

import pyautogui as pag

from src.common import Configuration, Move
from src.game.board import Board
from src.game.literals import GameState
from src.game.tile import Tile
from src.mediator.mediator import Mediator

Colour = Tuple[int, int, int]


TILE_SIZE = 16

SMILEY_WIDTH = 26
SMILEY_Y_OFFSET = 39

WHITE      = 255, 255, 255
GRAY       = 189, 189, 189
BLUE       =   0,   0, 255
DARK_GREEN =   0, 123,   0
RED        = 255,   0,   0
DARK_BLUE  =   0,   0, 123
DARK_RED   = 123,   0,   0
DARK_CYAN  =   0, 123, 123
BLACK      =   0,   0,   0
DARK_GRAY  = 123, 123, 123

NUMBER_PIXEL_X_OFFSET = 9
NUMBER_PIXEL_Y_OFFSET = 11

FLAG_PIXEL_X_OFFSET = 7
FLAG_PIXEL_Y_OFFSET = 3

SYMBOL_PIXEL_X_OFFSET = 6
SYMBOL_PIXEL_Y_OFFSET = 6

PIXEL_COLOUR_TO_MINE_COUNT: Dict[Colour, int] = {
    GRAY:       0,
    BLUE:       1,
    DARK_GREEN: 2,
    RED:        3,
    DARK_BLUE:  4,
    DARK_RED:   5,
    DARK_CYAN:  6,
    BLACK:      7,
    DARK_GRAY:  8
}

SMILEY_EYE_PIXEL_X_OFFSET = 11
SMILEY_EYE_PIXEL_Y_OFFSET = 10
SMILEY_GLASSES_PIXEL_X_OFFSET = 12
SMILEY_GLASSES_PIXEL_Y_OFFSET = 10


class WebPageMediator(Mediator):
    def __init__(self, configuration: Configuration) -> None:
        super().__init__(configuration)
        # TODO: make pyautogui quicker

    def observe_state(self) -> GameState:
        x0 = self._offsets.x + (self._dimensions.width * TILE_SIZE - SMILEY_WIDTH) // 2
        y0 = self._offsets.y - SMILEY_Y_OFFSET

        eye_pixel = pag.pixel(x0 + SMILEY_EYE_PIXEL_X_OFFSET, y0 + SMILEY_EYE_PIXEL_Y_OFFSET)
        if eye_pixel == BLACK:
            glasses_pixel = pag.pixel(x0 + SMILEY_GLASSES_PIXEL_X_OFFSET, y0 + SMILEY_GLASSES_PIXEL_Y_OFFSET)
            if glasses_pixel == BLACK:
                return 'victory'
            else:
                return 'inProgress'
        else:
            return 'failure'

    def observe_board(self, old_board: Board | None = None) -> Board:
        if old_board is not None:
            self._check_board_size(old_board)

        board = Board(self._dimensions.width, self._dimensions.height) \
            if old_board is None \
            else old_board

        for y in range(self._dimensions.height):
            for x in range(self._dimensions.width):
                tile = board[x, y]

                pixel_x = self._offsets.x + x * TILE_SIZE
                pixel_y = self._offsets.y + y * TILE_SIZE

                observe_tile(tile, pixel_x, pixel_y)

        return board

    def play(self, move: Move) -> None:
        pag.click(
            x=self._offsets.x + move.tile.x * TILE_SIZE + TILE_SIZE // 2,
            y=self._offsets.y + move.tile.y * TILE_SIZE + TILE_SIZE // 2,
            button=move.button
        )

    def reset(self) -> None:
        x = self._offsets.x + (self._dimensions.width * TILE_SIZE - SMILEY_WIDTH) // 2 + SMILEY_WIDTH // 2
        y = self._offsets.y - SMILEY_Y_OFFSET + SMILEY_WIDTH // 2

        pag.leftClick(x, y)

    def post_game_procedure(self) -> None:
        return


def observe_covered_tile(tile: Tile, x0: int, y0: int) -> None:
    potential_flag_pixel = pag.pixel(x0 + FLAG_PIXEL_X_OFFSET, y0 + FLAG_PIXEL_Y_OFFSET)

    if potential_flag_pixel == RED:
        tile.set_sign('FLAG')
    else:
        tile.set_sign('COVERED')


def observe_uncovered_tile(tile: Tile, x0: int, y0: int) -> None:
    number_pixel = pag.pixel(x0 + NUMBER_PIXEL_X_OFFSET, y0 + NUMBER_PIXEL_Y_OFFSET)

    if number_pixel == BLACK:
        symbol_pixel = pag.pixel(x0 + SYMBOL_PIXEL_X_OFFSET, y0 + SYMBOL_PIXEL_Y_OFFSET)

        if symbol_pixel == RED:
            tile.set_sign('BAD_MINE')
        elif symbol_pixel == WHITE:
            tile.set_sign('MINE')
        else:
            tile.set_count(PIXEL_COLOUR_TO_MINE_COUNT[number_pixel])
    else:
        mine_count = PIXEL_COLOUR_TO_MINE_COUNT.get(number_pixel)
        if mine_count is None:
            raise RuntimeError('observed unknown pixel colour')

        tile.set_count(mine_count)


def observe_tile(tile: Tile, x0: int, y0: int) -> None:
    corner_pixel = pag.pixel(x0 + 1, y0 + 1)

    if corner_pixel == RED:
        tile.set_sign('EXPLODED_MINE')
    elif corner_pixel == WHITE:
        observe_covered_tile(tile, x0, y0)
    else:
        observe_uncovered_tile(tile, x0, y0)
