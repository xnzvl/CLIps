from typing import Dict, List, Tuple

import pyautogui as pag

from src.common import BoardObservation, Configuration, GameState, TileObservation
from src.interactions.observer import Observer

Color = Tuple[int, int, int]


TILE_SIZE = 16

WHITE = 255, 255, 255
GRAY = 189, 189, 189
BLACK = 0, 0, 0
RED = 255, 0, 0

KEY_PIXEL_X_OFFSET = 9
KEY_PIXEL_Y_OFFSET = 10

COLOR_TO_TILE_OBSERVATION: Dict[Color, TileObservation] = {
    GRAY: ' ',
    (0, 0, 255): '1',
    (0, 123, 0): '2',
    (255, 0, 0): '3',
    (0, 0, 123): '4',
    (123, 0, 0): '5',
    (0, 123, 123): '6',
    (0, 0, 0): '7',
    (123, 123, 123): '8',
    (0, 0, 0): '+'
}


class WebPageObserver(Observer):
    def __init__(self, configuration: Configuration) -> None:
        super().__init__(configuration)

    def observe_state(self) -> GameState:
        pass # TODO

    def observe_board(self) -> BoardObservation:
        observation: BoardObservation = list()

        for y_tiles in range(self._dimensions.height):
            row: List[TileObservation] = list()

            for x_tiles in range(self._dimensions.width):
                pixel_x = self._offsets.x + x_tiles * TILE_SIZE
                pixel_y = self._offsets.y + y_tiles * TILE_SIZE

                tile_color = pag.pixel(pixel_x, pixel_y)

                if tile_color == WHITE:
                    row.append('O')
                elif tile_color == RED:
                    row.append('*')
                else:
                    tile = COLOR_TO_TILE_OBSERVATION.get(pag.pixel(pixel_x + KEY_PIXEL_X_OFFSET, pixel_y + KEY_PIXEL_Y_OFFSET))

                    if tile is None:
                        raise ValueError('Invalid color')

                    row.append(tile)

            observation.append(row)

        return observation
