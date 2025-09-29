from enum import Enum
from typing import Dict, Final, List, Literal, Never, Tuple, override

import pyautogui as pag
import PIL.Image

from src.common import Action, Move, MoveAction, WebPageSweeperConfiguration
from src.game.grids import GenericGrid, Grid
from src.game.sweeper import GameState, Sweeper, SweeperError
from src.game.tiles import MineCount, MutableTile, Symbol, Tile


MouseButton = Literal['right', 'middle', 'left']


class Colour(Enum):
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
    YELLOW     = 255, 255,   0


# TODO: create a structure from related constants? e.g. key pixels, emoji, digit

TILE_SIZE: Final = 16

NUMBER_PIXEL_X_OFFSET: Final = 9
NUMBER_PIXEL_Y_OFFSET: Final = 11

COVERED_KEY_PIXEL_X_OFFSET: Final = 7
COVERED_KEY_PIXEL_Y_OFFSET: Final = 3

SYMBOL_PIXEL_X_OFFSET: Final = 6
SYMBOL_PIXEL_Y_OFFSET: Final = 6

PIXEL_COLOUR_TO_MINE_COUNT: Final[Dict[Colour, MineCount]] = {
    Colour.BLUE:       1,
    Colour.DARK_GREEN: 2,
    Colour.RED:        3,
    Colour.DARK_BLUE:  4,
    Colour.DARK_RED:   5,
    Colour.DARK_CYAN:  6,
    Colour.BLACK:      7,
    Colour.DARK_GRAY:  8
}

EMOJI_WIDTH:    Final = 26
EMOJI_Y_OFFSET: Final = -39
EMOJI_EYE_PIXEL_X_OFFSET: Final = 11
EMOJI_EYE_PIXEL_Y_OFFSET: Final = 10
EMOJI_GLASSES_PIXEL_X_OFFSET: Final = 12
EMOJI_GLASSES_PIXEL_Y_OFFSET: Final = 10

COLOUR_AND_ACTION_TO_BUTTONS: Final[
    Dict[Tuple[Colour, MoveAction], Tuple[List[MouseButton] | None, List[MouseButton]]]
] = {
    (Colour.BLACK, Action.FLAG):          (None,              ['right', 'right']),
    (Colour.BLACK, Action.UNCOVER):       (None,              ['left']          ),
    (Colour.BLACK, Action.QUESTION_MARK): (None,              list()            ),
    (Colour.BLACK, Action.CLEAR):         (None,              ['right']         ),
    (Colour.RED,   Action.FLAG):          (list(),            list()            ),
    (Colour.RED,   Action.UNCOVER):       (['right', 'left'], ['right', 'left'] ),
    (Colour.RED,   Action.QUESTION_MARK): (None,              ['right']         ),
    (Colour.RED,   Action.CLEAR):         (['right'],         ['right', 'right']),
    (Colour.GRAY,  Action.FLAG):          (['right'],         ['right']         ),
    (Colour.GRAY,  Action.UNCOVER):       (['left'],          ['left']          ),
    (Colour.GRAY,  Action.QUESTION_MARK): (None,              ['right', 'right']),
    (Colour.GRAY,  Action.CLEAR):         (list(),            list()            ),
}

DIGIT_WIDTH:  Final = 13
DIGIT_HEIGHT: Final = 23
DIGIT_COUNT:  Final = 3

DIGIT_X_OFFSET: Final = 6
DIGIT_Y_OFFSET: Final = -38

DIGIT_SEGMENTS_HORIZONTAL_GAP: Final = 8
DIGIT_SEGMENTS_VERTICAL_GAP: Final = 10
DIGIT_SEGMENTS_HORIZONTAL_X_OFFSET: Final = 6
DIGIT_SEGMENTS_HORIZONTAL_Y_OFFSET: Final = 1
DIGIT_SEGMENTS_VERTICAL_X_OFFSET: Final = 2
DIGIT_SEGMENTS_VERTICAL_Y_OFFSET: Final = 6

DIGIT_SEGMENT_TUPLE_TO_CHAR: Final[
    Dict[Tuple[bool, bool, bool, bool, bool, bool, bool], str]
] = {
    (True,  True,  True,  True,  True,  True,  False): '0',
    (False, True,  True,  False, False, False, False): '1',
    (True,  True,  False, True,  True,  False, True ): '2',
    (True,  True,  True,  True,  False, False, True ): '3',
    (False, True,  True,  False, False, True,  True ): '4',
    (True,  False, True,  True,  False, True,  True ): '5',
    (True,  False, True,  True,  True,  True,  True ): '6',
    (True,  True,  True,  False, False, False, False): '7',
    (True,  True,  True,  True,  True,  True,  True ): '8',
    (True,  True,  True,  True,  False, True,  True ): '9',
    (False, False, False, False, False, False, True ): '-'
}  # boolean values are in order abcdefg according to 7-segment display


class WebPageSweeper(Sweeper[WebPageSweeperConfiguration]):
    @staticmethod
    def get_tile_size() -> int:
        return TILE_SIZE

    def __init__(self, configuration: WebPageSweeperConfiguration) -> None:
        super().__init__(configuration)

    @override
    def obtain_remaining_mines(self) -> int:
        digit_area = pag.screenshot(
            region=(
                self._configuration.offsets.x + DIGIT_X_OFFSET,
                self._configuration.offsets.y + DIGIT_Y_OFFSET,
                DIGIT_WIDTH * DIGIT_COUNT,
                DIGIT_HEIGHT
            )
        )
        return obtain_number(digit_area)


    @override
    def obtain_state(self) -> GameState:
        screen = pag.screenshot()

        x0 = self._configuration.offsets.x + (self._configuration.dimensions.width * TILE_SIZE - EMOJI_WIDTH) // 2
        y0 = self._configuration.offsets.y + EMOJI_Y_OFFSET

        # TODO: rest of the function is quite chaotic
        eye_colour = get_colour_from_pixel(screen, x0 + EMOJI_EYE_PIXEL_X_OFFSET, y0 + EMOJI_EYE_PIXEL_Y_OFFSET)
        if eye_colour == Colour.BLACK:
            glasses_pixel = get_colour_from_pixel(screen, x0 + EMOJI_GLASSES_PIXEL_X_OFFSET, y0 + EMOJI_GLASSES_PIXEL_Y_OFFSET)

            if glasses_pixel == Colour.YELLOW:
                return GameState.IN_PROGRESS
            elif glasses_pixel == Colour.BLACK:
                return GameState.VICTORY
            else:
                raise_unexpected_colour(eye_colour)
        elif eye_colour.value == (13, 12, 15):
            return GameState.VICTORY
        elif eye_colour == Colour.YELLOW:
            return GameState.FAILURE
        else:
            raise_unexpected_colour(eye_colour)

    @override
    def obtain_time(self) -> int:
        digit_area = pag.screenshot(
            region=(
                self._configuration.offsets.x + self._configuration.dimensions.width * TILE_SIZE - DIGIT_WIDTH * DIGIT_COUNT - DIGIT_X_OFFSET,
                self._configuration.offsets.y + DIGIT_Y_OFFSET,
                DIGIT_WIDTH * DIGIT_COUNT,
                DIGIT_HEIGHT
            )
        )
        return obtain_number(digit_area)

    @override
    def obtain_grid(self, old_grid: Grid[Tile] | None = None) -> Grid[Tile]:
        if old_grid is not None:
            self._check_grid_size(old_grid)

        dimensions = self._configuration.dimensions
        grid: Grid[Tile] = GenericGrid(dimensions, MutableTile) \
            if old_grid is None \
            else old_grid

        # TODO: screenshot only relevant area
        screen = pag.screenshot()

        for y in range(dimensions.height):
            for x in range(dimensions.width):
                tile = grid[x, y]

                pixel_x = self._configuration.offsets.x + x * TILE_SIZE
                pixel_y = self._configuration.offsets.y + y * TILE_SIZE

                observe_tile(screen, tile, pixel_x, pixel_y)

        return grid

    @override
    def play(self, move: Move) -> None:
        x0 = self._configuration.offsets.x + move.point.x * TILE_SIZE
        y0 = self._configuration.offsets.y + move.point.y * TILE_SIZE

        screenshot = pag.screenshot(
            region=(x0 + COVERED_KEY_PIXEL_X_OFFSET, y0 + COVERED_KEY_PIXEL_Y_OFFSET, 1, 1)
        )
        colour = get_colour_from_pixel(screenshot, 0, 0)

        result = COLOUR_AND_ACTION_TO_BUTTONS.get((colour, move.action))
        if result is None:
            raise_unexpected_colour(colour)

        buttons, buttons_with_question_marks = result
        if buttons is None:
            raise SweeperError('question marks aren\'t enabled')

        for b in (buttons_with_question_marks if self._configuration.question_marks else buttons):
            pag.click(
                x=x0 + TILE_SIZE // 2,
                y=y0 + TILE_SIZE // 2,
                button=b
            )

    @override
    def reset(self) -> None:
        x = self._configuration.offsets.x + (self._configuration.dimensions.width * TILE_SIZE - EMOJI_WIDTH) // 2 + EMOJI_WIDTH // 2
        y = self._configuration.offsets.y - EMOJI_Y_OFFSET + EMOJI_WIDTH // 2

        pag.leftClick(x, y)

    @override
    def sign_victory(self, name: str) -> None:  # TODO: not a fan of this implementation
        x0 = self._configuration.offsets.x + (self._configuration.dimensions.width * TILE_SIZE - EMOJI_WIDTH) // 2
        y0 = self._configuration.offsets.y - EMOJI_Y_OFFSET

        glasses_pixel = pag.pixel(x0 + EMOJI_GLASSES_PIXEL_X_OFFSET, y0 + EMOJI_GLASSES_PIXEL_Y_OFFSET)

        if glasses_pixel != Colour.YELLOW.value:
            pag.write(name, 0.1)
            pag.press('enter')


def raise_unexpected_pixel(pixel: float | tuple[int, ...] | None) -> Never:
    raise SweeperError(f'unexpected pixel - {pixel}')


def raise_unexpected_colour(colour: Colour) -> Never:
    raise SweeperError(f'unexpected colour - {colour.name}({colour.value})')


def get_colour_from_pixel(screen: PIL.Image.Image, x: int, y: int) -> Colour:
    pixel = screen.getpixel((x, y))

    if pixel is None:
        raise_unexpected_pixel(pixel)

    if type(pixel) == tuple and len(pixel) == 3:
        for colour in Colour:
            if colour.value == pixel:
                return colour

    raise_unexpected_pixel(pixel)


def observe_covered_tile(screen: PIL.Image.Image, tile: Tile, x0: int, y0: int) -> None:
    key_covered_colour = get_colour_from_pixel(screen, x0 + COVERED_KEY_PIXEL_X_OFFSET, y0 + COVERED_KEY_PIXEL_Y_OFFSET)

    if key_covered_colour == Colour.RED:
        tile.set_symbol(Symbol.FLAG)
    elif key_covered_colour == Colour.BLACK:
        tile.set_symbol(Symbol.QUESTION_MARK)
    else:
        tile.set_symbol(Symbol.COVER)


def observe_uncovered_tile(screen: PIL.Image.Image, tile: Tile, x0: int, y0: int) -> None:
    number_pixel_colour = get_colour_from_pixel(screen, x0 + NUMBER_PIXEL_X_OFFSET, y0 + NUMBER_PIXEL_Y_OFFSET)

    if number_pixel_colour == Colour.BLACK:
        symbol_pixel_colour = get_colour_from_pixel(screen, x0 + SYMBOL_PIXEL_X_OFFSET, y0 + SYMBOL_PIXEL_Y_OFFSET)

        if symbol_pixel_colour == Colour.RED:
            tile.set_symbol(Symbol.WRONG_FLAG)
        elif symbol_pixel_colour == Colour.WHITE:
            tile.set_symbol(Symbol.MINE)
        else:
            tile.set_symbol(Symbol.NUMBER, PIXEL_COLOUR_TO_MINE_COUNT[number_pixel_colour])

    else:
        if number_pixel_colour == Colour.GRAY:
            tile.set_symbol(Symbol.EMPTY)
            return

        mine_count = PIXEL_COLOUR_TO_MINE_COUNT.get(number_pixel_colour)

        if mine_count is None:
            raise_unexpected_colour(number_pixel_colour)

        tile.set_symbol(Symbol.NUMBER, mine_count)


def observe_tile(screen: PIL.Image.Image, tile: Tile, x0: int, y0: int) -> None:
    corner_colour = get_colour_from_pixel(screen, x0 + 1, y0 + 1)

    if corner_colour == Colour.RED:
        tile.set_symbol(Symbol.EXPLODED_MINE)
    elif corner_colour == Colour.WHITE:
        observe_covered_tile(screen, tile, x0, y0)
    elif corner_colour == Colour.GRAY:
        observe_uncovered_tile(screen, tile, x0, y0)
    else:
        raise_unexpected_colour(corner_colour)


def obtain_number(digits_area: PIL.Image.Image) -> int:
    return int(
        ''.join(
            [obtain_digit(digits_area, i) for i in range(DIGIT_COUNT)]
        )
    )


def obtain_digit(digits_area: PIL.Image.Image, digit_place_from_left: int) -> str:
    digit_offset = digit_place_from_left * DIGIT_WIDTH

    # TODO: this is horrendous
    segments = (
        is_digit_segment_on(digits_area, digit_offset + DIGIT_SEGMENTS_HORIZONTAL_X_OFFSET,                               DIGIT_SEGMENTS_HORIZONTAL_Y_OFFSET                                  ),
        is_digit_segment_on(digits_area, digit_offset + DIGIT_SEGMENTS_VERTICAL_X_OFFSET + DIGIT_SEGMENTS_HORIZONTAL_GAP, DIGIT_SEGMENTS_VERTICAL_Y_OFFSET                                    ),
        is_digit_segment_on(digits_area, digit_offset + DIGIT_SEGMENTS_VERTICAL_X_OFFSET + DIGIT_SEGMENTS_HORIZONTAL_GAP, DIGIT_SEGMENTS_VERTICAL_Y_OFFSET + DIGIT_SEGMENTS_HORIZONTAL_GAP    ),
        is_digit_segment_on(digits_area, digit_offset + DIGIT_SEGMENTS_HORIZONTAL_X_OFFSET,                               DIGIT_SEGMENTS_HORIZONTAL_Y_OFFSET + 2 * DIGIT_SEGMENTS_VERTICAL_GAP),
        is_digit_segment_on(digits_area, digit_offset + DIGIT_SEGMENTS_VERTICAL_X_OFFSET,                                 DIGIT_SEGMENTS_VERTICAL_Y_OFFSET + DIGIT_SEGMENTS_HORIZONTAL_GAP    ),
        is_digit_segment_on(digits_area, digit_offset + DIGIT_SEGMENTS_VERTICAL_X_OFFSET,                                 DIGIT_SEGMENTS_VERTICAL_Y_OFFSET                                    ),
        is_digit_segment_on(digits_area, digit_offset + DIGIT_SEGMENTS_HORIZONTAL_X_OFFSET,                               DIGIT_SEGMENTS_HORIZONTAL_Y_OFFSET + DIGIT_SEGMENTS_VERTICAL_GAP    )
    )

    digit = DIGIT_SEGMENT_TUPLE_TO_CHAR.get(segments)
    if digit is None:
        raise SweeperError(f'segments don\'t make up a digit nor minus sign - {segments}')

    return digit


def is_digit_segment_on(digit_area: PIL.Image.Image, x: int, y: int) -> bool:
    return get_colour_from_pixel(digit_area, x, y) == Colour.RED
