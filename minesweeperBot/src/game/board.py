from typing import List, Tuple

from src.game.symbol import Symbol
from src.game.tile import Tile


class Board:
    def __init__(self, width: int, height: int) -> None:
        if width < 1:
            raise ValueError(f'width has to be greater than 1 (provided {width})')
        if height < 1:
            raise ValueError(f'height has to be greater than 1 (provided {height})')

        self._width = width
        self._height = height
        self._tiles: List[List[Tile]] = [
            [Tile() for _ in range(width)]
            for _ in range(height)
        ]

    def __getitem__(self, key: Tuple[int, int]) -> Tile:
        x, y = key
        self._validate_position(x, y)
        return self._tiles[y][x]

    def _validate_position(self, x: int, y: int) -> None:
        if x < 0:
            raise IndexError('x cannot be lower than 0')
        if x >= self._width:
            raise IndexError(f'x cannot be greater than width of the board ({self._width})')

        if y < 0:
            raise IndexError('y cannot be lower than 0')
        if y >= self._height:
            raise IndexError(f'y cannot be greater than height of the board ({self._height})')

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height

    def get_tiles(self) -> List[List[Tile]]:
        return self._tiles

    def get_tile_at(self, x: int, y: int) -> Tile:
        return self[x, y]

    def get_neighbours_of_tile_at(self, x: int, y: int) -> List[Tile]:
        self._validate_position(x, y)
        neighbours: List[Tile] = list()

        for y_proximity in range(-1 if y != 0 else 0, 2 if y != self._height - 1 else 1):
            for x_proximity in range(-1 if x != 0 else 0, 2 if x != self._width - 1 else 1):
                if x_proximity == 0 and y_proximity == 0:
                    continue

                neighbours.append(self._tiles[y + y_proximity][x + x_proximity])

        return neighbours

    def is_valid(self) -> bool:
        # TODO: optional
        return False

    def print(self) -> None:
        for y in range(self._height):
            for x in range(self._width):
                print_tile(self[x, y])
            print()


def print_tile(tile: Tile) -> None:
    match tile.get_symbol():
        case Symbol.COVERED:
            to_print = 'O'
        case Symbol.EXPLODED_MINE:
            to_print = '*'
        case Symbol.MINE:
            to_print = '+'
        case Symbol.BAD_MINE:
            to_print = 'X'
        case Symbol.FLAG:
            to_print = 'F'
        case Symbol.QUESTION_MARK:
            to_print = '?'
        case Symbol.NUMBER:
            to_print = tile.get_count()
        case Symbol.EMPTY:
            to_print = ' '
        case _:
            raise RuntimeError('unhandled tile symbol')

    print(to_print, end='')
