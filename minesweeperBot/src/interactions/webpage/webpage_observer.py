from typing import Dict, Tuple

import pyautogui as pag

from src.common import Configuration, GameState
from src.game.board import Board
from src.game.symbol import Symbol
from src.game.tile import Tile
from src.interactions.observer import Observer


Colour = Tuple[int, int, int]


TILE_SIZE = 16

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


class WebPageObserver(Observer):
    def __init__(self, configuration: Configuration) -> None:
        super().__init__(configuration)

    def observe_state(self) -> GameState:
        pass # TODO

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


def observe_tile(tile: Tile, x: int, y: int) -> None:
    corner_pixel = pag.pixel(x + 1, y + 1)

    if corner_pixel == RED:
        tile.set_symbol(Symbol.EXPLODED_MINE)

    elif corner_pixel == WHITE:
        potential_flag_pixel = pag.pixel(x + FLAG_PIXEL_X_OFFSET, y + FLAG_PIXEL_Y_OFFSET)

        if potential_flag_pixel == RED:
            tile.set_symbol(Symbol.FLAG)
        else:
            tile.set_symbol(Symbol.COVERED)

    else:
        number_pixel = pag.pixel(x + NUMBER_PIXEL_X_OFFSET, y + NUMBER_PIXEL_Y_OFFSET)

        if number_pixel == BLACK:
            symbol_pixel = pag.pixel(x + SYMBOL_PIXEL_X_OFFSET, y + SYMBOL_PIXEL_Y_OFFSET)

            if symbol_pixel == RED:
                tile.set_symbol(Symbol.BAD_MINE)
            elif symbol_pixel == WHITE:
                tile.set_symbol(Symbol.MINE)
            else:
                tile.set_count(PIXEL_COLOUR_TO_MINE_COUNT[number_pixel])

        else:
            mine_count = PIXEL_COLOUR_TO_MINE_COUNT.get(number_pixel)

            if mine_count is None:
                raise RuntimeError('observed unknown pixel colour')

            tile.set_count(mine_count)
