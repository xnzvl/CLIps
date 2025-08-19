from abc import ABC
from typing import List, Tuple, override

from src.common import Dimensions, Point
from src.game.grids.grid import GridIterator, Grid
from src.game.tiles.impl.mutable_tile import MutableTile
from src.game.tiles.tile import Tile, tile_to_str


class ShapedGridIterator(GridIterator):
    def __init__(self, tiles: List[List[Tile]], dimensions: Dimensions) -> None:
        self._tiles = tiles
        self._dimensions = dimensions
        self._i = 0

    @override
    def __next__(self) -> Tuple[Point, Tile]:
        if self._i >= self._dimensions.width * self._dimensions.height:
            raise StopIteration

        x = self._i % self._dimensions.width
        y = self._i // self._dimensions.width
        self._i += 1

        return Point(x, y), self._tiles[y][x]


class ShapedGrid(Grid, ABC):
    def __init__(self, width: int, height: int) -> None:
        if width < 1:
            raise ValueError(f'width has to be greater than 1 (provided {width})')
        if height < 1:
            raise ValueError(f'height has to be greater than 1 (provided {height})')

        self._width = width
        self._height = height
        self._tiles: List[List[Tile]] = [
            [MutableTile() for _ in range(width)]
            for _ in range(height)
        ]

    @override
    def __iter__(self) -> GridIterator:
        return ShapedGridIterator(self._tiles, Dimensions(self._width, self._height))

    def _validate_position(self, x: int, y: int) -> None:
        if x < 0:
            raise IndexError('x cannot be lower than 0')
        if x >= self._width:
            raise IndexError(f'x cannot be greater than width of the board ({self._width})')

        if y < 0:
            raise IndexError('y cannot be lower than 0')
        if y >= self._height:
            raise IndexError(f'y cannot be greater than height of the board ({self._height})')

    @override
    def get_width(self) -> int:
        return self._width

    @override
    def get_height(self) -> int:
        return self._height

    @override
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

    @override
    def is_valid(self) -> bool:
        # TODO: seems easy, but it's quite tough
        #       also, it's optional
        return False

    @override
    def print(self) -> None:
        for y in range(self._height):
            for x in range(self._width):
                print(tile_to_str(self[x, y]), end='')
            print()
