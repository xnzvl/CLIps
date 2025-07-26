from typing import Tuple

import pyautogui as pag

from src.common import Configuration, GameState
from src.game.board import Board
from src.game.tile import Tile
from src.interactions.observer import Observer


TILE_SIZE = 16

WHITE = 255, 255, 255
GRAY = 189, 189, 189
BLACK = 0, 0, 0
RED = 255, 0, 0

KEY_PIXEL_X_OFFSET = 9
KEY_PIXEL_Y_OFFSET = 10


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

                observed_pixel = pag.pixel(pixel_x, pixel_y)

                if observed_pixel == WHITE:
                    tile.set_covered()
                elif observed_pixel == RED:
                    tile.place_mine(True)
                else:
                    update_tile_based_on_pixel(
                        tile,
                        pag.pixel(pixel_x + KEY_PIXEL_X_OFFSET, pixel_y + KEY_PIXEL_Y_OFFSET)
                    )

        return board


def update_tile_based_on_pixel(tile: Tile, pixel: Tuple[int, int, int]) -> None:
    match pixel:
        case 189, 189, 189:
            tile.set_empty()
        case 0, 0, 255:
            tile.set_count(1)
        case 0, 123, 0:
            tile.set_count(2)
        case 255, 0, 0:
            tile.set_count(3)
        case 0, 0, 123:
            tile.set_count(4)
        case 123, 0, 0:
            tile.set_count(5)
        case 0, 123, 123:
            tile.set_count(6)
        case 0, 0, 0:
            tile.set_count(7)
        case 123, 123, 123:
            tile.set_count(8)
        case _:
            raise ValueError('observed unexpected pixel colour')
