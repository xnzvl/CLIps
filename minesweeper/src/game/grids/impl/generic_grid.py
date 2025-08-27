from typing import Generator, List, Set, Tuple, override

from src.common import Dimensions, Point
from src.game.grids.grid import Grid, GridIterator
from src.game.tiles.impl.mutable_tile import MutableTile
from src.game.tiles.tile import Tile, tile_to_str, Symbol


class GenericGridIterator(GridIterator):
    def __init__(self, grid: Grid, dimensions: Dimensions) -> None:
        self._grid = grid
        self._dimensions = dimensions
        self._i = 0

    @override
    def __next__(self) -> Tuple[Point, Tile]:
        if self._i >= self._dimensions.width * self._dimensions.height:
            raise StopIteration

        x = self._i % self._dimensions.width
        y = self._i // self._dimensions.width
        self._i += 1

        return Point(x, y), self._grid[x, y]


class GenericGridNeighbourhoodIterator(GridIterator):
    def __init__(self, grid: Grid, dimensions: Dimensions, center: Point, radius: int, with_symbols: Tuple[Symbol, ...] = ()) -> None:
        self._generator = _create_generator(grid, dimensions, center, radius, set(with_symbols))

    @override
    def __next__(self) -> Tuple[Point, Tile]:
        return next(self._generator)


class GenericGrid(Grid):
    def __init__(self, dimensions: Dimensions) -> None:
        if dimensions.width < 1:
            raise ValueError(f'width has to be greater than 1 (provided {dimensions.width})')
        if dimensions.height < 1:
            raise ValueError(f'height has to be greater than 1 (provided {dimensions.height})')

        self._dimensions = dimensions
        self._tiles: List[List[Tile]] = ([
            [MutableTile() for _ in range(dimensions.width)]
            for _ in range(dimensions.height)
        ])

    @override
    def __getitem__(self, key: Tuple[int, int]) -> Tile:
        x, y = key
        self._validate_position(x, y)
        return self._tiles[y][x]

    @override
    def __iter__(self) -> GridIterator:
        return GenericGridIterator(self, self._dimensions)

    def _validate_position(self, x: int, y: int) -> None:  # TODO: could be a decorator?
        if x < 0:
            raise IndexError('x cannot be lower than 0')
        if x >= self._dimensions.width:
            raise IndexError(f'x cannot be greater than width of the grid ({self._dimensions.width})')

        if y < 0:
            raise IndexError('y cannot be lower than 0')
        if y >= self._dimensions.height:
            raise IndexError(f'y cannot be greater than height of the grid ({self._dimensions.height})')

    @override
    def get_width(self) -> int:
        return self._dimensions.width

    @override
    def get_height(self) -> int:
        return self._dimensions.height

    @override
    def neighbourhood_of(self, x: int, y: int) -> GridIterator:
        self._validate_position(x, y)
        return GenericGridNeighbourhoodIterator(self, self._dimensions, Point(x, y), 1)

    @override
    def neighbourhood_with_symbol_of(self, x: int, y: int, *desired_symbols: Symbol) -> GridIterator:
        self._validate_position(x, y)
        return GenericGridNeighbourhoodIterator(self, self._dimensions, Point(x, y), 1, desired_symbols)

    @override
    def wide_neighbourhood_of(self, x: int, y: int) -> GridIterator:
        self._validate_position(x, y)
        return GenericGridNeighbourhoodIterator(self, self._dimensions, Point(x, y), 2)

    @override
    def wide_neighbourhood_with_symbol_of(self, x: int, y: int, *desired_symbols: Symbol) -> GridIterator:
        self._validate_position(x, y)
        return GenericGridNeighbourhoodIterator(self, self._dimensions, Point(x, y), 2, desired_symbols)

    @override
    def is_valid(self) -> bool:
        # TODO: seems easy, but it's quite tough
        #       also, it's optional
        raise NotImplementedError()

    @override
    def print(self) -> None:
        for y in range(self._dimensions.height):
            for x in range(self._dimensions.width):
                print(tile_to_str(self[x, y]), end='')
            print()


def _create_generator(grid: Grid, dimensions: Dimensions, center: Point, radius: int, with_symbols: Set[Symbol]) -> Generator[Tuple[Point, Tile]]:
    center_x, center_y = center

    min_x = max(center_x - radius, 0)
    max_x = min(center_x + radius, dimensions.width - 1)
    min_y = max(center_y - radius, 0)
    max_y = min(center_y + radius, dimensions.height - 1)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if x == center_x and y == center_y:
                continue

            tile = grid[x, y]

            if not with_symbols or tile.get_symbol() in with_symbols:
                yield Point(x, y), tile
