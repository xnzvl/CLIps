from typing import Dict, Final, List, Literal, Never, Tuple, cast, override

import pyautogui as pag
import PIL.Image

from src.common import Action, Move, WebPageSweeperConfiguration
from src.exceptions import InvalidGameStateError
from src.game.grids.grid import Grid
from src.game.grids.impl.generic_grid import GenericGrid
from src.game.sweeper.sweeper import GameState, Sweeper
from src.game.tiles.tile import Tile


RGB = Tuple[int, int, int]
MouseButton = Literal['right', 'middle', 'left']


TILE_SIZE = 16

SMILEY_WIDTH = 26
SMILEY_Y_OFFSET = 39

# TODO: add final to all constants
WHITE: Final = 255, 255, 255
GRAY       = 189, 189, 189
BLUE       =   0,   0, 255
DARK_GREEN =   0, 123,   0
RED        = 255,   0,   0
DARK_BLUE  =   0,   0, 123
DARK_RED   = 123,   0,   0
DARK_CYAN  =   0, 123, 123
BLACK      =   0,   0,   0
DARK_GRAY  = 123, 123, 123
YELLOW     = 255, 255,   0

NUMBER_PIXEL_X_OFFSET = 9
NUMBER_PIXEL_Y_OFFSET = 11

COVERED_KEY_PIXEL_X_OFFSET = 7
COVERED_KEY_PIXEL_Y_OFFSET = 3

SYMBOL_PIXEL_X_OFFSET = 6
SYMBOL_PIXEL_Y_OFFSET = 6

PIXEL_COLOUR_TO_MINE_COUNT: Dict[RGB, int] = {
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

EMOJI_EYE_PIXEL_X_OFFSET = 11
EMOJI_EYE_PIXEL_Y_OFFSET = 10
EMOJI_GLASSES_PIXEL_X_OFFSET = 12
EMOJI_GLASSES_PIXEL_Y_OFFSET = 10

PIXEL_AND_ACTION_TO_BUTTONS: Dict[Tuple[RGB, Action], Tuple[List[MouseButton] | None, List[MouseButton]]] = {
    (BLACK, 'FLAG'):                (None,              ['right', 'right']),
    (BLACK, 'UNCOVER'):             (None,              ['left']          ),
    (BLACK, 'PLACE_QUESTION_MARK'): (None,              list()            ),
    (BLACK, 'CLEAR'):               (None,              ['right']         ),
    (RED,   'FLAG'):                (list(),            list()            ),
    (RED,   'UNCOVER'):             (['right', 'left'], ['right', 'left'] ),
    (RED,   'PLACE_QUESTION_MARK'): (None,              ['right']         ),
    (RED,   'CLEAR'):               (['right'],         ['right', 'right']),
    (GRAY,  'FLAG'):                (['right'],         ['right']         ),
    (GRAY,  'UNCOVER'):             (['left'],          ['left']          ),
    (GRAY,  'PLACE_QUESTION_MARK'): (None,              ['right', 'right']),
    (GRAY,  'CLEAR'):               (list(),            list()            ),
}


class WebPageSweeper(Sweeper):
    def __init__(self, configuration: WebPageSweeperConfiguration, with_question_marks: bool) -> None:
        super().__init__(configuration)

        self._offsets = configuration.offsets
        self._with_question_marks = with_question_marks

    @override
    def obtain_remaining_mines(self) -> int:  # TODO: implement
        return 99999

    @override
    def obtain_state(self) -> GameState:
        screen = pag.screenshot()

        x0 = self._offsets.x + (self._configuration.dimensions.width * TILE_SIZE - SMILEY_WIDTH) // 2
        y0 = self._offsets.y - SMILEY_Y_OFFSET

        # TODO: rest of the function is quite chaotic
        eye_pixel = get_rgb_from_pixel(screen, x0 + EMOJI_EYE_PIXEL_X_OFFSET, y0 + EMOJI_EYE_PIXEL_Y_OFFSET)
        if eye_pixel == BLACK:
            glasses_pixel = get_rgb_from_pixel(screen, x0 + EMOJI_GLASSES_PIXEL_X_OFFSET, y0 + EMOJI_GLASSES_PIXEL_Y_OFFSET)
            if glasses_pixel == YELLOW:
                return 'IN_PROGRESS'
            elif glasses_pixel == BLACK:
                return 'VICTORY'
            else:
                raise_unexpected_pixel(glasses_pixel)
        elif eye_pixel == (13, 12, 15):
            return 'VICTORY'
        elif eye_pixel == YELLOW:
            return 'FAILURE'
        else:
            raise_unexpected_pixel(eye_pixel)

    @override
    def obtain_time(self) -> int:
        pass

    @override
    def obtain_grid(self, old_grid: Grid | None = None) -> Grid:
        if old_grid is not None:
            self._check_grid_size(old_grid)

        dimensions = self._configuration.dimensions
        grid = GenericGrid(dimensions) \
            if old_grid is None \
            else old_grid

        # TODO: screenshot only relevant area
        screen = pag.screenshot()

        for y in range(dimensions.height):
            for x in range(dimensions.width):
                tile = grid[x, y]

                pixel_x = self._offsets.x + x * TILE_SIZE
                pixel_y = self._offsets.y + y * TILE_SIZE

                observe_tile(screen, tile, pixel_x, pixel_y)

        return grid

    @override
    def play(self, move: Move) -> None:
        x0 = self._offsets.x + move.tile.x * TILE_SIZE
        y0 = self._offsets.y + move.tile.y * TILE_SIZE

        screenshot = pag.screenshot(region=(x0 + COVERED_KEY_PIXEL_X_OFFSET, y0 + COVERED_KEY_PIXEL_Y_OFFSET, 1, 1))
        pixel = get_rgb_from_pixel(screenshot, 0, 0)

        result = PIXEL_AND_ACTION_TO_BUTTONS.get((pixel, move.action))
        if result is None:
            raise_unexpected_pixel(pixel)

        buttons, buttons_with_question_marks = result
        if buttons is None:
            raise InvalidGameStateError('question marks aren\'t enabled')

        for b in (buttons_with_question_marks if self._with_question_marks else buttons):
            pag.click(
                x=x0 + TILE_SIZE // 2,
                y=y0 + TILE_SIZE // 2,
                button=b
            )

    @override
    def reset(self) -> None:
        x = self._offsets.x + (self._configuration.dimensions.width * TILE_SIZE - SMILEY_WIDTH) // 2 + SMILEY_WIDTH // 2
        y = self._offsets.y - SMILEY_Y_OFFSET + SMILEY_WIDTH // 2

        pag.leftClick(x, y)

    @override
    def sign_victory(self, name: str) -> None:
        x0 = self._offsets.x + (self._configuration.dimensions.width * TILE_SIZE - SMILEY_WIDTH) // 2
        y0 = self._offsets.y - SMILEY_Y_OFFSET
        glasses_pixel = pag.pixel(x0 + EMOJI_GLASSES_PIXEL_X_OFFSET, y0 + EMOJI_GLASSES_PIXEL_Y_OFFSET)

        if glasses_pixel != YELLOW:
            pag.write(name, 0.1)
            pag.press('enter')


def raise_unexpected_pixel(pixel: float | tuple[int, ...] | None) -> Never:
    raise RuntimeError(f'unexpected pixel - {pixel}')


def get_rgb_from_pixel(screen: PIL.Image.Image, x: int, y: int) -> RGB:
    pixel = screen.getpixel((x, y))

    if pixel is None:
        raise_unexpected_pixel(pixel)

    if type(pixel) == tuple:
        tuple_pixel = cast(tuple[int, ...], pixel)

        if len(tuple_pixel) >= 3:
            return cast(RGB, tuple_pixel[:3])

    raise_unexpected_pixel(pixel)


def observe_covered_tile(screen: PIL.Image.Image, tile: Tile, x0: int, y0: int) -> None:
    key_covered_pixel = get_rgb_from_pixel(screen, x0 + COVERED_KEY_PIXEL_X_OFFSET, y0 + COVERED_KEY_PIXEL_Y_OFFSET)

    if key_covered_pixel == RED:
        tile.set_sign('FLAG')
    elif key_covered_pixel == BLACK:
        tile.set_sign('QUESTION_MARK')
    else:
        tile.set_sign('COVERED')


def observe_uncovered_tile(screen: PIL.Image.Image, tile: Tile, x0: int, y0: int) -> None:
    number_pixel = get_rgb_from_pixel(screen, x0 + NUMBER_PIXEL_X_OFFSET, y0 + NUMBER_PIXEL_Y_OFFSET)

    if number_pixel == BLACK:
        symbol_pixel = get_rgb_from_pixel(screen, x0 + SYMBOL_PIXEL_X_OFFSET, y0 + SYMBOL_PIXEL_Y_OFFSET)

        if symbol_pixel == RED:
            tile.set_sign('BAD_MINE')
        elif symbol_pixel == WHITE:
            tile.set_sign('MINE')
        else:
            tile.set_count(PIXEL_COLOUR_TO_MINE_COUNT[number_pixel])
    else:
        mine_count = PIXEL_COLOUR_TO_MINE_COUNT.get(number_pixel)
        if mine_count is None:
            raise_unexpected_pixel(number_pixel)

        tile.set_count(mine_count)


def observe_tile(screen: PIL.Image.Image, tile: Tile, x0: int, y0: int) -> None:
    corner_pixel = get_rgb_from_pixel(screen, x0 + 1, y0 + 1)

    if corner_pixel == RED:
        tile.set_sign('EXPLODED_MINE')
    elif corner_pixel == WHITE:
        observe_covered_tile(screen, tile, x0, y0)
    elif corner_pixel == GRAY:
        observe_uncovered_tile(screen, tile, x0, y0)
    else:
        raise_unexpected_pixel(corner_pixel)
