from typing import List, Tuple, assert_never

from src.common import Dimensions, Point
from src.game.tile import Tile


class BoardIterator:
    def __init__(self, tiles: List[List[Tile]], dimensions: Dimensions) -> None:
        self._tiles = tiles
        self._dimensions = dimensions
        self._i = 0

    def __next__(self) -> Tuple[Point, Tile]:
        if self._i >= self._dimensions.width * self._dimensions.height:
            raise StopIteration

        x = self._i % self._dimensions.width
        y = self._i // self._dimensions.width
        self._i += 1

        return Point(x, y), self._tiles[y][x]


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

    def __iter__(self) -> BoardIterator:
        return BoardIterator(self._tiles, Dimensions(self._width, self._height))

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

    def get_tile_at(self, x: int, y: int) -> Tile:
        return self[x, y]

    def get_neighbours_of_tile_at(self, x: int, y: int) -> List[Tuple[Point, Tile]]:
        self._validate_position(x, y)
        neighbours: List[Tuple[Point, Tile]] = list()

        for y_proximity in range(-1 if y != 0 else 0, 2 if y != self._height - 1 else 1):
            for x_proximity in range(-1 if x != 0 else 0, 2 if x != self._width - 1 else 1):
                if x_proximity == 0 and y_proximity == 0:
                    continue

                x_t = x + x_proximity
                y_t = y + y_proximity

                neighbours.append((Point(x_t, y_t), self[x_t, y_t]))

        return neighbours

    def is_valid(self) -> bool:
        # TODO: seems easy, but it's quite tough
        #       also, it's optional
        return False

    def print(self) -> None:
        for y in range(self._height):
            for x in range(self._width):
                print_tile(self[x, y])
            print()


def print_tile(tile: Tile) -> None:
    match tile.get_symbol():
        case 'COVERED':
            to_print = 'O'
        case 'EXPLODED_MINE':
            to_print = '*'
        case 'MINE':
            to_print = '+'
        case 'BAD_MINE':
            to_print = 'X'
        case 'FLAG':
            to_print = 'F'
        case 'QUESTION_MARK':
            to_print = '?'
        case 'NUMBER':
            to_print = tile.get_count()
        case 'EMPTY':
            to_print = ' '
        case _:
            assert_never(tile.get_symbol())

    print(to_print, end='')
